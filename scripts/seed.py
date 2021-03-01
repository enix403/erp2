from app.salary.models import (
    AppUser
)
from app.salary.core.auth import AuthRole
from app.salary.core import admin


class Seeder:
    def __init__(self):
        pass


    def seed(self):
        user = AppUser.make("Admin", "admin", "pass")
        user.college_id = -1
        user.role_param_id = 0
        user.auth_role = AuthRole.SUPERUSER
        user.staff_role = 0
        user.invalidate = 0
        user.save()

        self.add_subjects()


    def add_subjects(self):
        subjects = [
            "Physics",
            "English",
            "Urdu",
            "Islamiat",
            "Chemistry",
            "Mathematics",
        ]
        for s in subjects:
            admin.make_subject(s)



def run():
    seeder = Seeder()
    seeder.seed()
