from .manager import AuthManager
from .constants import PermissionType
from .execptions import HttpUnauthorized
from typing import Union
from ..models import College


def validate_college(college: Union[College, int]):
    user_cpk = AuthManager.user_college_pk()
        
    if user_cpk == 0:
        valid = True
    else:
        if isinstance(college, College):
            check_cpk = college.pk
        else:
            check_cpk = college
        valid = (user_cpk == check_cpk)
        
    if not valid:
        raise HttpUnauthorized()
    
    
def validate_read(target: str):
    if not AuthManager.permission_set().check_read(target):
        raise HttpUnauthorized
    
def validate_write(target: str):
    if not AuthManager.permission_set().check_write(target):
        raise HttpUnauthorized

def validate_edit(target: str):
    if not AuthManager.permission_set().check_edit(target):
        raise HttpUnauthorized
