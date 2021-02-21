from app.salary.models import (
    AppUser
)
from app.salary.core.auth import AuthRole

class Seeder:
    def __init__(self):
        pass


    def seed(self):
        user = AppUser.make("Admin", "admin", "pass")
        user.college_id = -1
        user.role_param_id = 0
        user.auth_role = AuthRole.SUPERUSER
        user.invalidate = 0
        user.save()


def run():
    seeder = Seeder()
    seeder.seed()



