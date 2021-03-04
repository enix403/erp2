from app.salary.typehints import HttpRequest
from .actions import handle_unauthorized


class PermissionCache:
    def __init__(self, request: HttpRequest, context):
        self.request = request
        self.context = context


        self.allowed = set()
        self.denied = set()

    def permits(self, permission):
        if permission in self.allowed:
            return True
        if permission in self.denied:
            return False

        result = self.request.auth_manager.permits(self.context, permission)
        if result:
            self.allowed.add(permission)
        else:
            self.denied.add(permission)

        return result

    def require_perm(self, context, *permissions):
        """Checks if the user has atleast one of the given permissions"""
        for perm in permissions:
            if self.permits(perm):
                return
        handle_unauthorized(self.request)
    
