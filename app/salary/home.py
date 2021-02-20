from django.shortcuts import redirect, reverse
from app.salary.typehints import HttpRequest

def root(req: HttpRequest):
    if req.auth_manager.user == None:
        return redirect(reverse('sl_u:Auth.Login'))
    else:
        return redirect(reverse('sl_u:Manage.Index'))