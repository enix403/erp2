from app.salary.core.auth.principals import PR_AuthRole, PR_ClgAccess
from app.salary.core.auth.authroles import AuthRole


def simple_access_principals(college_id):
    return ( 
        PR_ClgAccess(college_id),
        PR_AuthRole(AuthRole.SUPERUSER)
    )

def validate_simple(request, college_id):
    return request.auth_manager.require_one(simple_access_principals(college_id))