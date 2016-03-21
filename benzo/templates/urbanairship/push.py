from collections import OrderedDict

from benzo.template import Base


class Template(Base):
    def get_fields(self):
        fields = super(Template, self).get_fields()
        fields.update(
            OrderedDict([
                ('API_KEY', {}, ),
                ('PUSH_SECRET', {}, ),
            ])
        )

        return fields

    def get_headers(self):
        headers = super(Template, self).get_headers()
        headers.update({
            'Accept': 'application/vnd.urbanairship+json; version=3;',
        })

        return headers

    def get_template(self):
        return {
            'device_types': [],
            'message': {},
            'audience': {},
        }
