from app.salary.core.auth import Allow, PR_AuthRole, AuthRole


class ManagePermissions:
    __acl__ = (
        # fmt: off
        (Allow, PR_AuthRole(AuthRole.SUPERUSER), [  'station:create', 
                                                    'station:read',  ]),

        (Allow, PR_AuthRole(AuthRole.SUPERUSER), [  'clg:create', 
                                                    'clg:read', ]),
        # fmt: on
    )
