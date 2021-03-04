from django.shortcuts import redirect, reverse
from app.salary.typehints import HttpRequest
from app.salary.core.auth import AuthRole


def root(req: HttpRequest):
    user = req.auth_manager.user
    if user is None:
        return redirect(reverse('sl_u:Auth.Login'))
    else:
        authrole = user.auth_role

        if authrole == AuthRole.SUPERUSER:
            return redirect(reverse('sl_u:Manage.Index'))
        else:
            return redirect(reverse('sl_u:Staff.Index', args=[user.college_id]))
