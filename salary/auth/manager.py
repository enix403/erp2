from django.http import HttpRequest

from passlib.hash import pbkdf2_sha256

import base.helpers as helpers
from ..models import AppUser
from .constants import PermissionType


class PermissionSet:
    def __init__(self, user: AppUser):
        
        if user is not None:
            groups = list(map(lambda ug: ug.group, user.acl_user_groups.prefetch_related('group__perms')))
            perms = []
            for g in groups:
                perms.extend(g.perms.all())

            self._perms = perms
            
        else:
            self._perms = []

    def check_perm(self, ptype, target):

        if ptype == 'read':
            ptype = PermissionType.PERM_READ
        elif ptype == 'write':
            ptype = PermissionType.PERM_WRITE
        elif ptype == 'edit':
            ptype = PermissionType.PERM_EDIT

        for p in self._perms:
            if p.perm_type == ptype and (p.perm == target or p.perm == '*'):
                return True

        return False

    def check_read(self, target):
        return self.check_perm(PermissionType.PERM_READ, target)

    def check_write(self, target):
        return self.check_perm(PermissionType.PERM_WRITE, target)

    def check_edit(self, target):
        return self.check_perm(PermissionType.PERM_EDIT, target)


class AuthManager:
    _user: AppUser = None
    SESSION_USER_ID_KEY = 'sl_app_user_id'
    
    _perm_set: PermissionSet = PermissionSet(None)
    
    @classmethod
    def permission_set(cls):
        return cls._perm_set
    
    @classmethod
    def fill_from_session(cls, req: HttpRequest):
        user_id = helpers.to_int(req.session.get(cls.SESSION_USER_ID_KEY))
        
        if user_id != 0:
            user = AppUser.objects.filter(pk=user_id).first()
            cls._user = user
            cls._perm_set = PermissionSet(user)
        else:
            cls._user = None
            cls._perm_set = PermissionSet(None)

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
        
