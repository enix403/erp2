from __future__ import annotations
import datetime

from collections import namedtuple
from ..models import (
    RoleParam,
    Staff,
    Subject,
    FacSubject,
    Person,
    College,
)

from django.db.models import Q

from base import helpers

from .constants import StaffStatus
from . import roles


def add_staff_subject(staff: Staff, subject: Subject, main=1):
    fac_subject = FacSubject()
    fac_subject.staff = staff
    fac_subject.target_subject = subject
    fac_subject.main = main
    fac_subject.save()
    return fac_subject


StaffParamSet = namedtuple('StaffParamSet', [
    "transfer_date",
    'main_role',
    'main_subject',
])


def add_new_staff(college: College, person: Person, param_data: StaffParamSet):

    staff = Staff()
    staff.college = college
    staff.person = person
    staff.status = StaffStatus.ACTIVE
    staff.name = person.name

    staff.transfer_date = param_data.transfer_date
    staff.main_role = param_data.main_role.role
    staff.has_faculty = 1 if param_data.main_role.role == roles.ROLE_FACULTY else 0
    
    staff.save()

    return staff


RoleParamInfo = namedtuple('RoleParamInfo', [
    "role_info",
    "category",
    "w_agreed",
    "x_rate",
    "salary",
    'main',

    'date_start',
    'date_end',
])


def add_staff_role(college: College, staff: Staff, param_data: RoleParamInfo):
    role_param = RoleParam()
    role_param.staff = staff
    role_param.college = college
    role_param.role = param_data.role_info.role
    role_param.category = param_data.category
    role_param.w_agreed = param_data.w_agreed
    role_param.x_rate = param_data.x_rate
    role_param.salary = param_data.salary
    
    role_param.main = param_data.main
    role_param.active = 1

    role_param.date_start = param_data.date_start
    if param_data.date_end is not None:
        role_param.date_end = param_data.date_end

    role_param.save()

    return role_param

class StaffProcessor:
    def __init__(self, staff: Staff, date_start: datetime.date, date_end: datetime.date = None):

        self.date_start = date_start
        self.date_end = date_end

        if date_end is None or date_start == date_end:
            qs = staff.role_params.filter(
                date_end__gte=date_start,
                date_start__lte=date_start,
            )
        else:
            end_1 = Q(date_start__lte=self.date_start) & Q(date_end__gte=self.date_start)
            end_2 = Q(date_start__lte=self.date_end) & Q(date_end__gte=self.date_end)
            mid = Q(date_start__gte=self.date_start) & Q(date_end__lte=self.date_end)

            qs = staff.role_params.filter(
                end_1 | end_2 | mid,
            )

        self.role_params = list(qs)



    def find_date_params(self, date: datetime.date):
        params = []
        for rp in self.role_params: # type: RoleParam
            if date >= rp.date_start and date <= rp.date_end:
                params.append(rp)
            
        return params
    
    
    def find_faculty_param(self, date: datetime.date):
        return helpers.get_first([p for p in self.find_date_params(date) if p.role == roles.ROLE_FACULTY])

    
    
    
        