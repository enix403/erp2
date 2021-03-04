from __future__ import annotations
from django.http import HttpRequest

from app.base.utils import to_int, is_nonstr_iter
from app.salary.models import AppUser
from app.salary.core.exceptions import UserLogicException

from .principals import (
    Everyone,
    Authenticated,
    # StaffRole,
    PR_UserId,
    PR_AuthRole,
    PR_ClgAccess,
    PR_StaffRole
)

from .actions import Allow, Deny
from .interfaces import IAuthenticationPolicy, IAuthorizationPolicy


class SessionCookieAuthnPolicy(IAuthenticationPolicy):

    SESSION_KEY = "ss_tkt_userid"

    def unauthenticated_userid(self, request: HttpRequest):
        userid = request.session.get(self.SESSION_KEY)
        if not userid:
            return None

        userid = to_int(userid)
        if userid == 0:
            return None

        return userid

    def authenticated_user(self, request: HttpRequest):
        userid = self.unauthenticated_userid(request)
        if userid is None:
            return None

        user = AppUser.objects.filter(pk=userid).first()
        if user is None:
            return None

        return user

    def forget(self, request: HttpRequest):
        request.session[self.SESSION_KEY] = 0

    def remember(self, request: HttpRequest, userid):
        request.session[self.SESSION_KEY] = userid


class SimpleAuthPolicy(SessionCookieAuthnPolicy):
    def effective_principals(self, user: AppUser):
        principals = [Everyone]
        if user is not None:
            principals.append(Authenticated)
            principals.append(PR_UserId(user.id))
            principals.append(PR_AuthRole(user.auth_role))
            # principals.append(PR_StaffRole(user.role_param_id...))
            if user.college_id != -1:
                principals.append(PR_ClgAccess(user.college_id))

            if user.role_param_id != 0:
                principals.append(PR_StaffRole(user.staff_role))

        return tuple(principals)


class AclAuthorizationPolicy(IAuthorizationPolicy):
    def permits(self, context, principals, permission):
        acl = []
        try:
            acl = context.__acl__
        except AttributeError:
            return False

        if callable(acl):
            acl = acl()

        allowed = False

        for ace in acl:
            perm_action, perm_pcpl, perm_name = ace

            if not is_nonstr_iter(perm_name):
                perm_name = (perm_name,)

            if permission in perm_name:
                if perm_pcpl in principals:
                    if perm_action == Allow:
                        allowed = True
                    elif perm_action == Deny:
                        allowed = False
                    else:
                        # TODO: log error
                        pass

        return allowed
