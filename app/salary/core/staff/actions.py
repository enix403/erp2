from __future__ import annotations
import datetime
# from typing import NamedTuple

from collections import namedtuple
from app.salary.models import (
    RoleParam,
    Staff,
    Subject,
    FacSubject,
    Person,
    College,
)

from django.db.models import Q

from app.base import utils

from .constants import StaffStatus
from . import roles


def add_staff_subject(staff: Staff, subject: Subject, main=1):
    fac_subject = FacSubject()
    fac_subject.staff = staff
    fac_subject.target_subject = subject
    fac_subject.main = main
    # fac_subject.save()
    return fac_subject


StaffPayload = namedtuple('StaffPayload', [
    'activate_date',  # str
    'main_role',  # int
])

# class StaffPayload(NamedTuple):
# activate_date: str
# main_role: int
# main_subject: Subject


def add_new_staff(college: College, person: Person, payload: StaffPayload):

    staff = Staff()
    staff.college = college
    staff.person = person
    staff.status = StaffStatus.ACTIVE
    staff.name = person.name

    staff.transfer_date = datetime.date.today()
    staff.activate_date = payload.activate_date
    staff.main_role = payload.main_role

    staff.has_faculty = 1 if payload.main_role == roles.ROLE_FACULTY else 0

    # staff.save()

    return staff


RoleParamPayload = namedtuple('RoleParamPayload', [
    "role_info",  # int
    "category",
    "w_agreed",
    "x_rate",
    "salary",
    'is_main',

    'date_start',
])


def add_staff_role(college: College, staff: Staff, param_data: RoleParamPayload):
    role_param = RoleParam()
    role_param.staff = staff
    role_param.college = college
    role_param.role = param_data.role_info.role
    role_param.category = param_data.category
    role_param.w_agreed = param_data.w_agreed
    role_param.x_rate = param_data.x_rate
    role_param.salary = param_data.salary

    role_param.main = param_data.is_main
    role_param.active = 1

    role_param.date_start = param_data.date_start

    # role_param.save()

    return role_param

# class StaffProcessor:
#     def __init__(self, staff: Staff, date_start: datetime.date, date_end: datetime.date = None):

#         self.date_start = date_start
#         self.date_end = date_end

#         if date_end is None or date_start == date_end:
#             qs = staff.role_params.filter(
#                 date_end__gte=date_start,
#                 date_start__lte=date_start,
#             )
#         else:
#             end_1 = Q(date_start__lte=self.date_start) & Q(date_end__gte=self.date_start)
#             end_2 = Q(date_start__lte=self.date_end) & Q(date_end__gte=self.date_end)
#             mid = Q(date_start__gte=self.date_start) & Q(date_end__lte=self.date_end)

#             qs = staff.role_params.filter(
#                 end_1 | end_2 | mid,
#             )

#         self.role_params = list(qs)


#     def filter_date_params(self, date: datetime.date):
#         params = []
#         for rp in self.role_params: # type: RoleParam
#             if date >= rp.date_start and date <= rp.date_end:
#                 params.append(rp)

#         return params


#     def facultyparam(self, date: datetime.date):
#         return utils.lst_first([p for p in self.filter_date_params(date) if p.role == roles.ROLE_FACULTY])
