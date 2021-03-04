from . import roles
from app.salary.core.auth import (
    Allow,
    Deny,
    PR_AuthRole,
    PR_StaffRole,
    AuthRole
)


class StaffPermissions:
    __acl__ = [
        (Allow, PR_AuthRole(AuthRole.SUPERUSER), ('staff:read', 'staff:create')),
        (Allow, PR_AuthRole(AuthRole.CLGSTAFF), 'staff:read'),  # All college staff can read

        (Allow, PR_StaffRole(roles.ROLE_PRINCIPLE), 'staff:create')  # Principal can also add staff
    ]
