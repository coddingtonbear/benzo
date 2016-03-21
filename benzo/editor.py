from __future__ import print_function

import subprocess
import os
import tempfile


def benzo_request(template, formatter):
    base_template = get_base_template(template, formatter)

    with tempfile.NamedTemporaryFile(
        suffix=formatter.get_extension()
    ) as out:
        out.write(base_template)
        out.flush()

        spawn_editor(out.name)

        out.seek(0)
        contents = out.read()

    fields, headers, body = parse_contents(contents, formatter)

    response = template.dispatch_request(fields, headers, body)

    print(response.content)


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
