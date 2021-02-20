from django.http import HttpRequest

from .interfaces import (
    IAuthenticationPolicy,
    IAuthorizationPolicy
)
# from app.salary.models import AppUser


class AuthManager:
    def __init__(
        self,
        request: HttpRequest,
        authn_policy: IAuthenticationPolicy,
        authz_policy: IAuthorizationPolicy
    ):

        self.user = authn_policy.authenticated_user(request) # type: AppUser
        self.user_principals = authn_policy.effective_principals(self.user) # type: list

        self.authn_policy = authn_policy
        self.authz_policy = authz_policy


    def permits(self, context, permission):
        """Returns True if the permission is allowed in the given context, False otherwise"""
        return self.authz_policy.permits(context, self.user_principals, permission)

    def refresh_principals(self):
        self.user_principals = self.authn_policy.effective_principals(self.user)

    def require_one(self, principals):
        """Returns True the user has any of the principals, False otherwise"""
        return any(p in self.user_principals for p in principals)

    def require_all(self, principals):
        """Returns True the user has all of the principals, False otherwise"""
        return all(p in self.user_principals for p in principals)

    def require(self, principal):
        """Checks wether tbe user has the principal"""
        return principal in self.user_principals

