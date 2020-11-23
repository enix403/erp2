#!/usr/bin/env python

from ..logic import admin, college as l_college
from ..logic.constants import Gender, FacultyCategory
from ..logic import roles
from ..auth import users

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

        # s = admin.make_station("Lahore")
        # cl = l_college.Impl_College.make_college("LBC1", s)
        # cl_impl = l_college.Impl_College(cl)
        # cl_impl.add_regular_section('PMG1')
        # cl_impl.add_regular_section('PMG2')
        # cl_impl.add_regular_section('PMG3')
        # cl_impl.add_regular_section('PMG4')
        # cl_impl.add_regular_section('PMG5')
        # cl_impl.add_regular_section('PMG6')

        # self.add_staff(cl_impl)
        self.add_user(None, 1)


    def add_user(self, c, r):

        users.make_user(None, None, 0, users.UserInfo("Admin", "admin", "pass"))
        # users.make_user(c, r, 1, users.UserInfo("User 1", "user1", "pass"))

        # u = AppUser.make("Admin", "admin", "pass")
        # u.college_id = 0
        # u.role_param_id = 0
        # u.type = 0
        # u.save()

        # u = AppUser.make("User 1", "user1", "pass")
        # u.college_id = c.pk
        # u.role_param_id = r
        # u.type = 1
        # u.save()

    # def add_staff(self, cl_impl: l_college.Impl_College):
        # cl_impl.add_staff(l_college.Impl_College.StaffParamSet(
        #     'ABC',
        #     234453,
        #     53464,
        #     Gender.MALE,
        #     roles.ROLE_FACULTY,
        #     Subject.objects.first(),
        #     FacultyCategory.FAC_CATERGORY_M,
        #     4,100, 3000,
        #     "2020-12-12",
        #     "2020-12-12",
        #     454
        # ))

        # cl_impl.add_staff(l_college.Impl_College.StaffParamSet(
        #     'XYZ',
        #     234453,
        #     53464,
        #     Gender.MALE,
        #     roles.ROLE_FACULTY,
        #     Subject.objects.first(),
        #     FacultyCategory.FAC_CATERGORY_M,
        #     4, 100, 3000,
        #     "2020-12-12",
        #     "2020-12-12",
        #     454
        # ))

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
