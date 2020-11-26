from django import template
from ..auth.manager import AuthManager
from ..auth.constants import PermissionType

import base.helpers as helpers

register = template.Library()


def _type_to_int(t):
    return helpers.to_int(t, None)


@register.simple_tag
def check_type(*types):
    res = AuthManager.is_type(*list(map(_type_to_int, types)))
    return res


@register.simple_tag
def user_college_pk():
    return AuthManager.user_college_pk()


def str_to_perm_type(permstr):
    if permstr == 'read':
        return PermissionType.PERM_READ
    if permstr == 'write':
        return PermissionType.PERM_WRITE
    if permstr == 'modify':
        return PermissionType.PERM_MODIFY

    return -1


@register.simple_tag
def auth_check(target, *ptypes):
    perm_set = AuthManager.permission_set()
    res = any(perm_set.check_perm(str_to_perm_type(ptype), target) for ptype in ptypes)
    return res
    
    
    