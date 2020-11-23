from .manager import AuthManager
from .execptions import UnauthorizedCollegeAccess
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
        raise UnauthorizedCollegeAccess()
    
    
