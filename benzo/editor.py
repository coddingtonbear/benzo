from __future__ import print_function

import subprocess
import os
import tempfile

from . import exceptions, sessions
from .template import get_installed_templates
from .formatter import get_installed_formatters


def benzo_request(template_name, formatter_name, session_path=None):
    all_templates = get_installed_templates()
    all_formatters = get_installed_formatters()

    if session_path is not None and os.path.exists(session_path):
        session_data = sessions.read_session(session_path)

        template = session_data['template']
        formatter = session_data['formatter']

        base_template = session_data['base_template']
        session = session_data['session']
    else:
        template = all_templates[template_name]()
        formatter = all_formatters[formatter_name]()

        base_template = get_base_template(template, formatter)
        session = template.get_session()

    with tempfile.NamedTemporaryFile(
        suffix=formatter.get_extension()
    ) as out:
        out.write(base_template)
        out.flush()

        spawn_editor(out.name)

        out.seek(0)
        contents = out.read()

        if not contents.strip():
            raise exceptions.RequestAborted()

        if session_path:
            sessions.write_session(
                session_path,
                {
                    'template': template,
                    'formatter': formatter,
                    'base_template': contents,
                    'session': session,
                }
            )

    fields, headers, body = parse_contents(contents, formatter)

    return template.dispatch_request(session, fields, headers, body)


def get_base_template(template, formatter):
    lines = []

    fields = template.get_fields()
    for field_name, _ in fields.items():
        lines.append(
            u'{name}: {value}'.format(
                name=field_name,
                value=template.get_default_field_value(field_name)
            )
        )

    headers = template.get_headers()
    for header, value in headers.items():
        lines.append(
            u'[Header] {header}: {value}'.format(
                header=header,
                value=template.get_default_header_value(header),
            )
        )

    template_body = formatter.to_string(template.get_template())

    return u'\n'.join(
        [formatter.COMMENT_CHAR + ' ' + line for line in lines] +
        [template_body]
    )


def spawn_editor(path):
    subprocess.check_call(
        [
            os.environ.get('EDITOR', 'vim'),
            path,
        ]
    )


def parse_contents(body, formatter):
    fields = {}
    headers = {}
    body_lines = []

    lines = body.split('\n')
    in_preamble = True
    for line in lines:
        if line.startswith(formatter.COMMENT_CHAR) and in_preamble:
            line = line.lstrip(formatter.COMMENT_CHAR).strip()
            if line.lower().startswith('[header]'):
                line = line[8:]
                header_name, header_value = line.split(':', 1)
                headers[header_name.strip()] = header_value.strip()
            else:
                field_name, field_value = line.split(':', 1)
                fields[field_name.strip()] = field_value.strip()
        elif in_preamble:
            in_preamble = False
        if not in_preamble:
            body_lines.append(line)

    body = formatter.to_python(u'\n'.join(body_lines).strip())

    return fields, headers, body
