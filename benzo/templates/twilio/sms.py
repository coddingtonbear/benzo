from collections import OrderedDict

from benzo.template import Base


class Template(Base):
    API_VERSION = 'Twilio API Version'
    ACCOUNT_SID = 'Twilio Account SID'
    AUTH_TOKEN = 'Twilio Auth Token'
    OUTPUT_FORMATTER = 'form'

    def get_fields(self):
        fields = super(Template, self).get_fields()

        del fields['URL']
        fields.update(
            OrderedDict([
                (
                    self.API_VERSION,
                    {
                        'default': self.get_config_value(
                            'twilio',
                            'api_version',
                            '2010-04-01',
                        )
                    }
                ),
                (
                    self.ACCOUNT_SID,
                    {
                        'default': self.get_config_value(
                            'twilio',
                            'account_sid',
                        )
                    }
                ),
                (
                    self.AUTH_TOKEN,
                    {
                        'default': self.get_config_value(
                            'twilio',
                            'auth_token',
                        )
                    }
                )
            ])
        )

        return fields

    def get_request_url(self, fields):
        return (
            'https://api.twilio.com/{api_version}'
            '/Accounts/{account_sid}/Messages.json'.format(
                api_version=fields[self.API_VERSION],
                account_sid=fields[self.ACCOUNT_SID],
            )
        )

    def get_request_headers(self, fields, headers):
        headers = super(Template, self).get_request_headers(fields, headers)
        self.add_basic_authorization_header(
            headers, fields[self.ACCOUNT_SID], fields[self.AUTH_TOKEN],
        )
        return headers

    def get_template(self):
        return {
            'From': self.get_config_value(
                'twilio',
                'default_from',
                '',
            ),
            'To': '',
            'Body': '',
        }
