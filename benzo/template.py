from collections import OrderedDict
import pkg_resources


class Base(object):
    FIELD_NAMES = {}

    def get_fields(self):
        return OrderedDict([
            ('URL', {}, ),
            ('PORT', {}, ),
            ('METHOD', {'default': 'POST'}, ),
        ])

    def get_default_field_value(self, field_name):
        fields = self.get_fields()
        
        default = fields.get(field_name, {}).get('default')
        if default is not None:
            return default

        return u''

    def get_headers(self):
        return {
            'Content-Type': 'application/json',
        }

    def get_default_header_value(self, header_name):
        headers = self.get_headers()

        return headers.get(header_name, '')

    def get_template(self):
        return {}


def get_installed_templates():
    all_templates = {}

    for entry_point in (
        pkg_resources.iter_entry_points(group='benzo_templates')
    ):
        try:
            loaded_class = entry_point.load()
        except ImportError:
            continue
        if not issubclass(loaded_class, Base):
            continue
        all_templates[entry_point.name] = loaded_class

    return all_templates
