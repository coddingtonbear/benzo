class RequestFailed(Exception):
    def __init__(
        self, message, result=None, fields=None, headers=None, body=None
    ):
        super(RequestFailed, self).__init__(message)

        self.result = result
        self.fields = fields
        self.headers = headers
