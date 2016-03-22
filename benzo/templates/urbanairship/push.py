from collections import OrderedDict

from benzo.template import Base


class Template(Base):
    APP_KEY = 'Urban Airship App Key'
    MASTER_SECRET = 'Urban Airship Master Secret'
    OUTPUT_FORMATTER = 'json'

    def get_fields(self):
        fields = super(Template, self).get_fields()
        fields.update(
            OrderedDict([
                (
                    'URL',
                    {
                        'default': self.get_config_value(
                            'urbanairship',
                            'push_url',
                            'https://go.urbanairship.com/api/push/',
                        )
                    },
                ),
                (
                    self.APP_KEY,
                    {
                        'default': self.get_config_value(
                            'urbanairship',
                            'app_key',
                        ),
                    },
                ),
                (
                    self.MASTER_SECRET,
                    {
                        'default': self.get_config_value(
                            'urbanairship',
                            'master_secret',
                        ),
                    },
                ),
            ])
        )

        return fields

    def get_request_headers(self, fields, headers):
        headers = super(Template, self).get_request_headers(fields, headers)
        self.add_basic_authorization_header(
            headers, fields[self.APP_KEY], fields[self.MASTER_SECRET],
        )
        return headers

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
