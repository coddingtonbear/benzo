from collections import OrderedDict
import os

from benzo.template import Base


class Template(Base):
    API_KEY = 'Urban Airship API Key'
    MASTER_SECRET = 'Urban Airship Master Secret'
    OUTPUT_FORMATTER = 'json'

    def get_fields(self):
        fields = super(Template, self).get_fields()
        fields.update(
            OrderedDict([
                (
                    'URL',
                    {
                        'default': os.environ.get(
                            'UA_PUSH_URL',
                            'https://go.urbanairship.com/api/push/',
                        )
                    },
                ),
                (
                    self.API_KEY,
                    {
                        'default': os.environ.get('UA_API_KEY'),
                    },
                ),
                (
                    self.MASTER_SECRET,
                    {
                        'default': os.environ.get('UA_MASTER_SECRET'),
                    },
                ),
            ])
        )

        return fields

    def get_request_headers(self, fields, headers):
        headers = super(Template, self).get_request_headers(fields, headers)
        self.add_basic_authorization_header(
            headers, fields[self.API_KEY], fields[self.MASTER_SECRET],
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
