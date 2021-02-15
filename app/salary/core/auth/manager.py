from django.http import HttpRequest

from .interfaces import (
    IAuthenticationPolicy,
    IAuthorizationPolicy
)
from .principals import ClgAccess

from app.salary.models import AppUser


class AuthManager:
    def __init__(
        self,
        request: HttpRequest,
        authn_policy: IAuthenticationPolicy,
        authz_policy: IAuthorizationPolicy
    ):

        userid = authn_policy.unauthenticated_userid(request)
        self.user = authn_policy.authenticated_user(userid) # type: AppUser
        self.user_principals = authn_policy.effective_principals(self.user) # type: list


    # def permits(self, context, permission, target_clg_id=None):
        # if target_clg_id != None and 
