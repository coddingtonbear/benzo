from __future__ import print_function

import argparse

from . import editor, formatter, template


def main():
    all_templates = template.get_installed_templates()
    all_formatters = formatter.get_installed_formatters()

    parser = argparse.ArgumentParser()
    parser.add_argument(
        'template',
        nargs=1,
        choices=all_templates.keys(),
    )
    parser.add_argument(
        '--editor-format',
        '-f',
        dest='editor_format',
        default='json',
        choices=all_formatters.keys()
    )
    args = parser.parse_args()

    result = editor.benzo_request(
        template=all_templates[args.template[0]](),
        formatter=all_formatters[args.editor_format]()
    )
    print(result)
