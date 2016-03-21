import base64
from collections import OrderedDict
import json
import pkg_resources
import pprint

import requests

from . import exceptions


class Base(object):
    FIELD_NAMES = {}

    def get_session(self):
        return requests.Session()

    def get_fields(self):
        return OrderedDict([
            ('Method', {'default': 'POST'}, ),
            ('URL', {}, ),
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

    def get_request_url(self, fields):
        return fields['URL']

    def get_request_method(self, fields):
        return fields['Method']

    def add_basic_authorization_header(self, headers, username, password):
        headers['Authorization'] = 'Basic ' + base64.b64encode(
            u'{username}:{password}'.format(
                username=username,
                password=password,
            ).encode('utf8')
        )

    def get_request_headers(self, fields, headers):
        return headers

    def get_request_body(self, fields, body):
        return body

    def get_request_result(self, session, fields, headers, body):
        return session.request(
            self.get_request_method(fields),
            self.get_request_url(fields),
            headers=self.get_request_headers(fields, headers),
            data=json.dumps(
                self.get_request_body(fields, body)
            ),
        )

    def dispatch_request(self, session, fields, headers, body):
        result = self.get_request_result(session, fields, headers, body)

        if not result.ok:
            raise exceptions.RequestFailed(
                result.text,
                result,
                fields,
                headers,
                body,
            )

        return result, pprint.pformat(result.json(), indent=4)


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
