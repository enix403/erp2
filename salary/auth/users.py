from __future__ import annotations
from typing import Optional



from ..models import (
    AppUser,
    College,
    RoleParam
)

from collections import namedtuple

UserInfo = namedtuple("UserInfo", ['name', 'username', 'password'])


def make_user(college: Optional[College], role_param: Optional[RoleParam], m_type: int, info: UserInfo):
    user_model = AppUser.make(info.name, info.username, info.password)
    user_model.college_id = 0 if college is None else college.pk
    if isinstance(role_param, int):
        user_model.role_param_id = role_param
    else:
       user_model.role_param_id = 0 if role_param is None else role_param.pk
    user_model.type = m_type
    user_model.save()
    
    return user_model
    
