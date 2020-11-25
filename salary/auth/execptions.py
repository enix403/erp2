class HttpResponseErrorCode(Exception):
    def __init__(self, code, msg="An error occured"):
        self.code = code
        self.msg = msg


class HttpUnauthorized(HttpResponseErrorCode):
    def __init__(self):
        super().__init__(401, 'Not Authorized')

