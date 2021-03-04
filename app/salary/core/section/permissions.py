from app.salary.core.auth import (
    Allow,
    AuthRole,
    PR_AuthRole,
    PR_StaffRole
)

from app.salary.core.staff import roles

all_permissions = (
    'reg_sec:create',
    'meg_sec:create',
    'reg_sec:read',
    'meg_sec:read'
)

class SectionPermissions:
    __acl__ = (
        # fmt: off
        (Allow, PR_AuthRole(AuthRole.SUPERUSER), all_permissions),
        (Allow, PR_StaffRole(roles.ROLE_PRINCIPLE), all_permissions),
        # fmt: on
    )
