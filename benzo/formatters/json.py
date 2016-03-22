from __future__ import absolute_import

import json

from benzo.formatter import Base


class Formatter(Base):
    CONTENT_TYPE = 'application/json'

    def to_string(self, value):
        if not value:
            return ''

        return json.dumps(
            value,
            indent=4,
            sort_keys=True,
        )

    def get_extension(self):
        return '.json'

    def to_python(self, value):
        if not value.strip():
            return None

        return json.loads(value)
