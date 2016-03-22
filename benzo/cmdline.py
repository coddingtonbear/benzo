from __future__ import print_function

import argparse
import sys
import os
import pdb
import traceback

from blessings import Terminal
import six

from . import config, editor, exceptions, formatter, template


def main():
    terminal = Terminal()

    all_templates = template.get_installed_templates()
    all_formatters = formatter.get_installed_formatters()

    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--template',
        dest='template',
        default=None,
        choices=all_templates.keys(),
    )
    parser.add_argument(
        '--session',
        '-s',
        dest='session_path',
        default=None,
    )
    parser.add_argument(
        '--editor-format',
        '-f',
        dest='editor_format',
        default=None,
        choices=all_formatters.keys()
    )
    parser.add_argument(
        '--debugger',
        '-d',
        dest='debugger',
        default=False,
        action='store_true',
    )
    args = parser.parse_args()

    exit_code = 0
    if args.session_path and os.path.exists(args.session_path):
        if args.template or args.editor_format:
            parser.error(
                "You cannot set a template or editor format when "
                "resuming a pre-existing session."
            )
    elif args.template and args.template not in all_templates:
        parser.error(
            "Template '{name}' does not exist.".format(
                name=args.template,
            )
        )

    conf = config.get_config()
    default_template_name = (
        conf.get('benzo', {}).get('default_template', 'json')
    )
    default_formatter_name = (
        conf.get('benzo', {}).get('default_editor_format', 'json')
    )
    try:
        result, response = editor.benzo_request(
            template_name=args.template or default_template_name,
            formatter_name=args.editor_format or default_formatter_name,
            session_path=args.session_path,
        )
    except exceptions.RequestFailed as e:
        print(
            u"{t.bold}{t.red}Request failed (status: {status})!{t.normal} "
            u"{t.red}{message}{t.normal}".format(
                t=terminal,
                status=e.result.status_code,
                message=six.text_type(e)
            )
        )
        exit_code = 2
    except Exception as e:
        print(
            u"{t.bold}{t.red}Unhandled exception occurred:{t.normal} "
            u"{t.red}{message}\n"
            "{traceback}{t.normal}".format(
                t=terminal,
                message=six.text_type(e),
                traceback=traceback.format_exc()
            )
        )
        exit_code = 1
    else:
        print(
            u"{t.green}{message}{t.normal}".format(
                t=terminal,
                message=response,
            )
        )

    if args.debugger:
        pdb.set_trace()

    sys.exit(exit_code)
