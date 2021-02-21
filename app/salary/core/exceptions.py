class UserLogicException(Exception):
    def __init__(self, user_msg="An error occured", route_name=None, route_args=[], query_params=''):
        self.user_msg = user_msg
        self.route_name = route_name
        self.route_args = route_args
        self.query_params = query_params

class HttpResponseErrorCode(Exception):
    def __init__(self, code, msg="Error"):
        self.code = code
        self.msg = msg

class HttpUnauthorized(HttpResponseErrorCode):
    def __init__(self, msg='Not Authorized'):
        super().__init__(401, msg)


class HttpNotFound(HttpResponseErrorCode):
    def  __init__(self, msg='Not Found'):
        super().__init__(404, msg)


class HttpRedirectException(Exception):
    def __init__(self, url, permanent=False):
        self.permanent = permanent
        self.url = url
