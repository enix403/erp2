from __future__ import annotations
from django.http import HttpRequest as _Req

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .core.auth.manager import AuthManager


class HttpRequest(_Req):
    auth_manager: AuthManager

