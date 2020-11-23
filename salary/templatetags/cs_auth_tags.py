from django import template
from ..auth.manager import AuthManager

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
    