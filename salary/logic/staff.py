from collections import namedtuple
from ..models import (
    RoleParam_v2,
    Staff_v2,
    Subject,
    FacSubject_v2,
    Person,
    College,
)

from .constants import StaffStatus
from . import roles


def add_staff_subject(staff: Staff_v2, subject: Subject, main=1):
    fac_subject = FacSubject_v2()
    fac_subject.staff = staff
    fac_subject.target_subject = subject
    fac_subject.main = main
    fac_subject.save()
    return fac_subject




StaffParamSet = namedtuple('StaffParamSet', [
    # "erp_number",
    # "name",
    # "cnic",
    # "bank_acc",
    # "gender",
    # 'init_date',
    "transfer_date",
    'main_role',
    
    'main_subject',
])


"""
from salary.logic import roles
from salary.logic.staff import *
p = Person.objects.get(pk=4)
c = College.objects.first()
fac = roles.role_from_id(roles.ROLE_FACULTY)

sb = Subject.objects.first()
sps = StaffParamSet('2020-10-12', fac, sb)

st = add_new_staff(c, p, sps)
"""

def add_new_staff(college: College, person: Person, param_data: StaffParamSet):

    # person = Person()
    # person.erp_number = param_data.erp_number
    # person.name = param_data.name
    # person.cnic = param_data.cnic
    # person.gender = param_data.gender
    # person.bank_acc = param_data.bank_acc
    # person.j_date_kips = param_data.init_date
    # person.save()

    staff = Staff_v2()
    staff.college = college
    staff.person = person
    staff.status = StaffStatus.ACTIVE

    staff.transfer_date = param_data.transfer_date
    staff.main_role = param_data.main_role.role
    
    staff.save()
    
    if param_data.main_role.role == roles.ROLE_FACULTY:
        add_staff_subject(staff, param_data.main_subject, 1)


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

"""
rps = RoleParamInfo(
    fac,
    1,
    4,
    400,
    600,
    1,
    '2020-10-12',
    None
)

"""


def add_staff_role(college: College, staff: Staff_v2, param_data: RoleParamInfo):
    role_param = RoleParam_v2()
    role_param.staff = staff
    # role_param.name = param_data.name
    role_param.college = college
    role_param.role = param_data.role_info.role
    role_param.category = param_data.category
    role_param.w_agreed = param_data.w_agreed
    role_param.x_rate = param_data.x_rate
    role_param.salary = param_data.salary
    
    role_param.main = param_data.main
    role_param.active = 1

    role_param.date_start = param_data.date_start
    role_param.date_end = param_data.date_end

    role_param.save()

    return role_param
