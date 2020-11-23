from ..models import AppUser
from django.http import HttpRequest

import base.helpers as helpers

from passlib.hash import pbkdf2_sha256


class AuthManager:
    _user: AppUser = None
    SESSION_USER_ID_KEY = 'sl_app_user_id'
    
    @classmethod
    def fill_from_session(cls, req: HttpRequest):
        user_id = helpers.to_int(req.session.get(cls.SESSION_USER_ID_KEY))
        
        if user_id != 0:
            user = AppUser.objects.filter(pk=user_id).first()
            cls._user = user
        else:
            cls._user = None

    @classmethod
    def get_logged_in_user(cls):
        return cls._user

    @classmethod
    def set_logged_in_user(cls, req: HttpRequest, user: AppUser):
        if user is not None:
            req.session[cls.SESSION_USER_ID_KEY] = user.pk
        else:
            req.session[cls.SESSION_USER_ID_KEY] = 0
        cls._user = user
        
    @staticmethod
    def find_from_username(username):
        return AppUser.objects.filter(username=username).first()
    
    @classmethod
    def login_get_user(cls, username, password):
        user = cls.find_from_username(username)
    
        if user is not None:
            if pbkdf2_sha256.verify(password, user.password_hash):
                if user.invalidate != 0:
                    user.invalidate = 0
                    user.save()
                return user
        
        return None
    
        
    
    @classmethod
    def user_college_pk(cls):
        user = cls.get_logged_in_user()
        if user is None:
            return -1
        return user.college_id
        
        
    @classmethod
    def is_type(cls, *types):
        user: AppUser = cls.get_logged_in_user()
        if user is not None:
            return user.is_type(*types)
        return False
        