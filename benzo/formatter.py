import pkg_resources


class Base(object):
    COMMENT_CHAR = '#'

    def to_string(self, value):
        raise NotImplementedError()

    def to_python(self, value):
        raise NotImplementedError()

    def get_extension(self):
        return '.txt'


def get_installed_formatters():
    all_templates = {}

    for entry_point in (
        pkg_resources.iter_entry_points(group='benzo_formatters')
    ):
        try:
            loaded_class = entry_point.load()
        except ImportError:
            continue
        if not issubclass(loaded_class, Base):
            continue
        all_templates[entry_point.name] = loaded_class

    return all_templates
