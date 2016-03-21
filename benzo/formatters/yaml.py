from __future__ import absolute_import

import yaml

from benzo.formatter import Base


class Formatter(Base):
    def to_string(self, value):
        return yaml.dump(
            value,
            default_flow_style=False,
        )

    def to_python(self, value):
        return yaml.load(value)

    def get_extension(self):
        return '.yaml'
