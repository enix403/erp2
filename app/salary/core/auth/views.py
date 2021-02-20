from __future__ import annotations
from django.shortcuts import render, redirect, reverse
from django.views import View

from app.salary.typehints import HttpRequest
from app.salary.core.exceptions import UserLogicException



class LoginView(View):
    def get(self, request: HttpRequest):
        if request.auth_manager.user == None:
            return render(request, 'sl/login.html')
        return redirect('/')

    def post(self, request: HttpRequest):
        bag = request.POST

        username = bag.get('username', '')
        password = bag.get('password', '')

        if request.auth_manager.login(username, password):
            return redirect('/')

        raise UserLogicException('Username or password is incorrect') 


def logout_view(request: HttpRequest):
    request.auth_manager.logout()
    return redirect(reverse('sl_u:Auth.Login'))