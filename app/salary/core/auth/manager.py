from passlib.hash import pbkdf2_sha256
from django.http import HttpRequest

from .interfaces import IAuthenticationPolicy, IAuthorizationPolicy
from app.salary.core.auth import handle_unauthorized
from app.salary.models import AppUser


class AuthManager:
    def __init__(
        self,
        request: HttpRequest,
        authn_policy: IAuthenticationPolicy,
        authz_policy: IAuthorizationPolicy,
    ):

        self.request = request
        self.user = authn_policy.authenticated_user(request)  # type: AppUser
        self.user_principals = authn_policy.effective_principals(
            self.user
        )  # type: list

        self.authn_policy = authn_policy
        self.authz_policy = authz_policy

    def require_permissions_one(self, context, *permissions):
        """Checks if the user has atleast one of the given permissions"""
        for perm in permissions:
            permits = self.authz_policy.permits(context, self.user_principals, perm)
            if permits:
                return
        handle_unauthorized(self.request)

    def permits(self, context, permission):
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


    def login(self, username, password):
        user = AppUser.objects.filter(username=username).first()

        if user is None:
            return False

        if not pbkdf2_sha256.verify(password, user.password_hash):
            return False

        if user.invalidate != 0:
           user.invalidate = 0
           user.save()

        self.authn_policy.remember(self.request, user.pk)
        self.user = user
        self.refresh_principals()

        return True

    
    def logout(self):
        self.authn_policy.forget(self.request)
        self.user = None
        self.refresh_principals()