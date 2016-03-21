from __future__ import absolute_import

import json

from benzo.formatter import Base


class Formatter(Base):
    def to_string(self, value):
        return json.dumps(
            value,
            indent=4,
            sort_keys=True,
        )

    def get_extension(self):
        return '.json'

    def to_python(self, value):
        return json.loads(value)
