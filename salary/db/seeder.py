#!/usr/bin/env python

from ..logic import admin, college as l_college
from ..logic.constants import Gender, FacultyCategory
from ..logic import roles
from ..auth import users
from ..auth.constants import AuthUserType


from ..models import (
    Subject,
    AppUser,
    
    
    # AclGroup,
    # AclUserGroup,
    # AclGroupPermission,
    # AclUserPermission
    
)


class Seeder:
    def run(self):
        self.add_subjects()

        s = admin.make_station("Lahore")
        cl = l_college.Impl_College.make_college("LBC1", s)
        cl_impl = l_college.Impl_College(cl)
        cl_impl.add_regular_section('PMG1')
        cl_impl.add_regular_section('PMG2')
        cl_impl.add_regular_section('PMG3')
        cl_impl.add_regular_section('PMG4')
        cl_impl.add_regular_section('PMG5')
        cl_impl.add_regular_section('PMG6')

        self.add_user(None, 1)


    def add_user(self, c, r):
        users.make_user(None, None, AuthUserType.ROOT, users.UserInfo("Admin", "admin", "pass"))
    
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


def exec():
    seeder = Seeder()
    seeder.run()
