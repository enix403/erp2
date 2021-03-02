from app.salary.core.auth.principals import PR_AuthRole, PR_ClgAccess
from app.salary.core.auth.authroles import AuthRole
from app.salary.core.auth import handle_unauthorized


def simple_access_principals(college_id):
    return ( 
        PR_ClgAccess(college_id),
        PR_AuthRole(AuthRole.SUPERUSER)
    )

def college_validate_simple(request, college_id):
    has_access = request.auth_manager.require_one(simple_access_principals(college_id))
    if not has_access:
        handle_unauthorized(request)