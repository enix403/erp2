from __future__ import annotations
import re


from django.shortcuts import render, redirect, reverse
from django.views import View
from django.http import HttpRequest, Http404
from django.contrib import messages

from .execptions import DisplayToUserException
import base.helpers as helpers

from ..auth.manager import AuthManager
from ..auth.validation import validate_college
from ..auth import users
from ..controllers.execptions import DisplayToUserException

from ..models import (
    # College,
    RoleParam,
    AppUser
)


def view_login(req):
    
    if AuthManager.get_logged_in_user() == None:
        return render(req, "sl/pages/login.html", {})
    return redirect('/')


class Action_Login(View):
    def post(self, req):
        bag = helpers.get_bag(req)
        username = bag.get('username', '')
        password = bag.get('password', '')
        
        login_user = AuthManager.login_get_user(username, password)
        if login_user is not None:
            AuthManager.set_logged_in_user(req, login_user)
            return redirect('/')
        
        raise DisplayToUserException('Invalid username or password')
    
    
class Action_Logout(View):
    def _handle(self, req: HttpRequest):
        AuthManager.set_logged_in_user(req, None)
        req.session.flush()
        return redirect('/')
    
    def get(self, req):
        return self._handle(req)
    
    def post(self, req):
        return self._handle(req)
        
        

def get_rp_and_college(rp_id):
    role_param = RoleParam.objects.filter(pk=rp_id).select_related('college').first()
    if role_param is not None:
        college = role_param.college
    else:
        college = None
        
    return role_param, college    
        
class UserAccountsView(View):
    def get(self, req, role_param_id):

        # role_param = RoleParam.objects.filter(pk=role_param_id).select_related('college').first()
        # if role_param is None:
        #     raise Http404
        # college = role_param.college
        
        role_param, college = get_rp_and_college(role_param_id)
        if role_param is None:
            # raise DisplayToUserException("Staff not found")
            raise Http404
        
        
        validate_college(college)
        
        return render(req, "sl/pages/create-user.html", {
            'college': college,
            'role_param': role_param
        })
        
        
        
        
        
class Action_CreateUser(View):
    def post(self, req):
        bag = helpers.get_bag(req)
        
        role_param_id = helpers.to_int(bag.get("role_param_id"))
        
        # role_param = RoleParam.objects.filter(pk=role_param_id).select_related('college').first()
        # if role_param is None:
        #     raise DisplayToUserException("Staff not found")
        # college = role_param.college
        
        role_param, college = get_rp_and_college(role_param_id)
        if role_param is None:
            raise DisplayToUserException("Staff not found")
        
        validate_college(college)
        m_type = 1
            
        username = str(bag.get("username", '')).strip()
        password = str(bag.get("password", ''))
        conf_password = str(bag.get("conf_password", ''))
        
        if password != conf_password:
            raise DisplayToUserException("Passwords do not match")

        
        if not username or not password:
            raise DisplayToUserException("Please fill all fields")
        
        
        if not re.match(r'[a-zA-Z0-9.]+$', username):
            raise DisplayToUserException("Invalid username")
        
        if AppUser.objects.filter(username=username).exists():
            raise DisplayToUserException("Username not available")
        
        if role_param.user_acc_exists():
            raise DisplayToUserException("Account for this role already exists")
            
        
        
        users.make_user(college, role_param, m_type, users.UserInfo(role_param.name, username, password))
        
        messages.success(req, "User added successfully")
        return redirect(reverse('sl_u:view-staff', args=[college.pk]))
        
        

            
        
            
            
        
        

