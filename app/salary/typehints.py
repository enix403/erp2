from django.http import HttpRequest as _Req
from .core.auth.manager import AuthManager

class HttpRequest(_Req):
    auth_manager: AuthManager
    