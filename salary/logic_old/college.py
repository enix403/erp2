from __future__ import annotations
from ..models import (
    Station,
    College,
    Section,
    MergeSectionRow,
    Person,
    Staff,
    RoleParam,
    FacSubject,
    Subject
)
from collections import namedtuple

# from . import exceptions as excp
from .constants import SectionType, StaffStatus
from . import roles



class Impl_College(object):

    def __init__(self, src: College):
        self.src = src

    @staticmethod
    def make_college(name: str, station: Station):
        college = College()
        college.name = name
        college.station = station
        college.save()
        return college
    
    
    #*************SECTIONS*************#
    
    
    def _make_section(self, name, type, active=1):
        section = Section()
        section.name = name
        section.m_type = type
        section.active = active
        section.college = self.src

        return section
    

    def add_regular_section(self, name):
        section = self._make_section(name, SectionType.REGULAR)
        section.save()
        return section
    
    # TODO: wrap in transaction
    def add_merged_section(self, name: str, children: list):
        parent_section: Section = self._make_section(name, SectionType.MERGED)
        parent_section.save()

        merge_rows_bulk = []

        for child in children:  # type: Section
            row = MergeSectionRow()
            row.parent_section = parent_section
            row.target_section = child

            merge_rows_bulk.append(row)

        MergeSectionRow.objects.bulk_create(merge_rows_bulk)

        return parent_section

    #*************STAFF*************#

    StaffParamSet = namedtuple('StaffParamSet', [
        "name", 
        "cnic", 
        "bank_acc", 
        "gender",
        # "role_info", 
        # "subject", 
        # "category", 
        # "w_agreed", 
        # "x_rate", 
        # "salary", 
        "j_date_kips", 
        # "j_date_campus", 
        "erp_number",
    ])

    RoleParamInfo = namedtuple('RoleParamInfo', [
        'name',
        "role_info",
        "subject",
        "category",
        "w_agreed",
        "x_rate",
        "salary",
        "j_date_campus",
        'main'
    ])


    def add_role_subject(self, faculty_param: RoleParam, subject: Subject, main=1):
        fac_subject = FacSubject()
        fac_subject.faculty_param = faculty_param
        fac_subject.target_subject = subject
        fac_subject.main = main
        fac_subject.save()
        return fac_subject


    # TODO: wrap in transaction
    def add_staff(self, param_data: StaffParamSet):
        person = Person()
        person.erp_number = param_data.erp_number
        person.name = param_data.name
        person.cnic = param_data.cnic
        person.gender = param_data.gender
        person.bank_acc = param_data.bank_acc
        person.j_date_kips = param_data.j_date_kips
        person.save()

        staff = Staff()
        staff.college = self.src
        staff.person = person
        staff.status = StaffStatus.ACTIVE
        staff.save()
        
        return staff




    def add_staff_role(self, staff: Staff, param_data: RoleParamInfo):
        role_param = RoleParam()
        role_param.j_date_campus = param_data.j_date_campus
        role_param.staff = staff
        role_param.name = param_data.name
        role_param.college = self.src
        role_param.role = param_data.role_info.role
        role_param.w_agreed = param_data.w_agreed
        role_param.x_rate = param_data.x_rate
        role_param.category = param_data.category
        role_param.salary = param_data.salary
        role_param.active = 1
        
        role_param.main = param_data.main
        
        role_param.save()
        
        if param_data.role_info.role == roles.ROLE_FACULTY:
            self.add_role_subject(role_param, param_data.subject)
        
        return role_param

      
