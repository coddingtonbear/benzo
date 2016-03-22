import urllib

from benzo.formatter import Base


class Formatter(Base):
    CONTENT_TYPE = 'application/x-www-form-urlencoded'

    def to_string(self, value):
        return urllib.urlencode(value)

    def get_extension(self):
        return '.txt'
