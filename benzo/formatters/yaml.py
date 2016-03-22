from __future__ import absolute_import

import yaml

from benzo.formatter import Base


class Formatter(Base):
    CONTENT_TYPE = 'application/json'

    def to_string(self, value):
        if not value:
            return ''

        return yaml.dump(
            value,
            default_flow_style=False,
        )

    def to_python(self, value):
        if not value:
            return None

        return yaml.load(value)

    def get_extension(self):
        return '.yaml'
