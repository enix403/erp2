from django import template

from app.salary.typehints import HttpRequest
from app.salary.core.staff import roles
from app.salary.core.auth import AuthRole


MAINLINKS = {
    AuthRole.SUPERUSER: ['manage'],
    AuthRole.CLGSTAFF: {
        roles.ROLE_PRINCIPLE: ['staff', 'section']
    }
}


register = template.Library()

"""
https://docs.djangoproject.com/en/3.1/howto/custom-template-tags/#simple-tags

"The first argument must be called context"
"""
@register.simple_tag(takes_context=True) # noqa
def getpagelinks(context):
    request = context['request'] # type: HttpRequest
    user = request.auth_manager.user
    if user is None:
        return { 'LK_UserType': None }

    authrole = user.auth_role

    if authrole == AuthRole.SUPERUSER:
        usertype = 'su'
        main_links = MAINLINKS[AuthRole.SUPERUSER]
    else:
        usertype = 'clg'
        main_links = MAINLINKS[AuthRole.CLGSTAFF].get(user.staff_role, [])

    return {
        'TL_UserCollegeID': user.college_id,
        'LK_UserType': usertype,
        'LK_MainLinks': main_links,
        'LK_ReportLinks': []
    }

