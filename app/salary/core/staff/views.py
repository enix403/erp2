from __future__ import annotations
from django.shortcuts import render, redirect, reverse
from django.views import View
from django.contrib import messages
from django.http import Http404
from django.db import transaction

from dateutil import parser as datetime_parser
import datetime

from app.base import utils, datetimeformat
from app.salary.typehints import HttpRequest
from app.salary.core.exceptions import UserLogicException

from app.salary.models import (
    College,
    Subject,
    Person,
    Staff,
    RoleParam,
)

from . import actions, roles
from .constants import (
    FacultyCategory,
    Gender,
    StaffStatus
)

from app.salary.core.college import clg_validate_simple
from app.salary.core.auth import Allow, PR_AuthRole, PR_StaffRole, AuthRole


class StaffPermissions:
    __acl__ = [
        (Allow, PR_AuthRole(AuthRole.SUPERUSER), ('staff:read', 'staff:create')),
        (Allow, PR_StaffRole(roles.ROLE_PRINCIPLE), ('staff:read', 'staff:create')),
        (Allow, PR_AuthRole(AuthRole.CLGSTAFF), 'staff:read')
    ]


class StaffView(View):

    def roleparam_info(self, param: RoleParam):
        is_faculty = param.role == roles.ROLE_FACULTY
        
        main_suffix = ' (Main)' if param.main == 1 else ''

        return {
            'is_faculty': is_faculty,
            'role': roles.roleinfo(param.role).name + main_suffix,

            'subject': 'Math' if is_faculty else '-',
            'fac_category': 'Morning' if is_faculty else '-',
            'workload': param.w_agreed if is_faculty else '-',
            'xrate': param.x_rate if is_faculty else '-',
            'salary': '{:,}'.format(param.salary)
        }
        

    def staff_info(self, staff: Staff):
        active_roleparams = []
        for rp in staff.role_params.all():  # type: RoleParam
            if rp.active == 1:
                active_roleparams.append(rp)

        return {
            'name': staff.name,
            'cnic': staff.person.cnic,
            'gender': 'Male' if staff.person.gender == Gender.MALE else 'Female',
            
            'rp_count': len(active_roleparams),
            'roleparams': [self.roleparam_info(r) for r in active_roleparams]
        }


    def staff_list(self, college: College):

        staff_qs = college.staffs.all() \
                        .select_related('person') \
                        .prefetch_related('role_params', 'fac_subjects')

        return [self.staff_info(s) for s in staff_qs]  # TODO: filter staff

    def get(self, req: HttpRequest, college_id):
        req.auth_manager.require_perm(StaffPermissions, 'staff:create', 'staff:read')
        clg_validate_simple(req, college_id)

        college = College.objects.filter(pk=utils.to_int(college_id)).first()

        if college is None:
            raise Http404

        return render(req, 'sl/staff/st-main.html', {
            'college': college,
            'college_staffs': self.staff_list(college),
            'Gender': Gender,
            'all_roles': roles.all_roles(),
            'subjects': Subject.objects.all(),
            'FacultyCategory': FacultyCategory,
            'today': datetime.date.today().strftime(datetimeformat.DATE_USER_INPUT)
        })



class ValidateRoleParamMixin:
    def get_rpinfo(self, bag, is_main, date_start):
        role_info = roles.roleinfo(utils.to_int(bag.get('role')))
        category = utils.to_int(bag.get('category'))
        w_agreed = utils.to_int(bag.get('w_agreed'))
        x_rate = utils.to_int(bag.get('x_rate'))
        salary = utils.to_int(bag.get('salary'))

        rpinfo = actions.RoleParamPayload(
            role_info,
            category,
            w_agreed,
            x_rate,
            salary,
            is_main,
            
            date_start,
        )

        return rpinfo

    def validate_rpinfo(self, college, rpinfo: actions.RoleParamPayload):
        if rpinfo.role_info is None:
            raise UserLogicException("Invalid role")

        # TODO: handle duplicates

        # if not rpinfo.role_info.duplicate:
        #     if college.role_params.filter(role=rpinfo.role_info.role, active=1).exists():
        #         raise UserLogicException("A staff member with role of \"%s\" already exists" % rpinfo.role_info.name)

        if rpinfo.role_info.role == roles.ROLE_FACULTY:

            if not FacultyCategory.is_valid(rpinfo.category):
                raise UserLogicException("Invalid category")

            if rpinfo.w_agreed <= 0:
                raise UserLogicException("Invalid workload")

            if rpinfo.x_rate <= 0:
                raise UserLogicException("Invalid rate")

            if rpinfo.category == FacultyCategory.FAC_CATERGORY_V:
                # No salary for a visiting faculty
                rpinfo.salary = 0

            elif rpinfo.salary <= 0:
                raise UserLogicException("Invalid salary")

        elif rpinfo.salary <= 0:
            raise UserLogicException("Invalid salary")



class Action_CreateStaff(View, ValidateRoleParamMixin):

    def post(self, req: HttpRequest):
        bag = req.POST
        
        college_id = utils.to_int(bag.get('college_id'))
        college: College = College.objects.filter(pk=college_id).first()
        
        if college is None:
            raise UserLogicException("College not found")
        
        # validate_college(college)

        name = bag.get('name')
        cnic = bag.get('cnic')
        bank_acc = bag.get('bank_acc')
        gender = utils.to_int(bag.get('gender'))
        erp_number = utils.to_int(bag.get('erp_number'))
        

        try:
            # init_date = datetime_parser.parse(
            #     bag.get('init_date'),
            # ).date
            init_date = datetime.datetime.strptime(
                bag.get('init_date'),
                datetimeformat.DATE_USER_INPUT
            ).date()
        except:
            init_date = None
            
        try:
            # activate_date = datetime_parser.parse(
            #     bag.get('init_date'),
            # ).date
            activate_date = datetime.datetime.strptime(
                bag.get('activate_date'),
                datetimeformat.DATE_USER_INPUT
            ).date()
        except:
            activate_date = None

        fill_all = False
        if not name or not cnic or not bank_acc:
            fill_all = True
        if not init_date or not activate_date:
            fill_all = True

        if erp_number <= 0:
            fill_all = True

        if fill_all:
            raise UserLogicException("Please fill all fields")

        if gender != Gender.MALE and gender != Gender.FEMALE:
            raise UserLogicException("Invalid gender")
        
        
        rpinfo = self.get_rpinfo(bag, 1, activate_date)
        self.validate_rpinfo(college, rpinfo)
        
        if rpinfo.role_info.role == roles.ROLE_FACULTY:
            # subject = Subject.objects.filter(pk=utils.to_int(bag.get('subject_id'))).first()
            # if subject is None:
                # raise UserLogicException("Invalid subject")
            pass
            
        else:
            subject = None


        # TODO: handle duplicate ERP Number

        staff_payload = actions.StaffPayload(
            activate_date,
            rpinfo.role_info.role,
        )


        try:
            with transaction.atomic():
                person = Person()
                person.comp_number = erp_number
                person.name = name
                person.cnic = cnic
                person.gender = gender
                person.bank_acc = bank_acc
                person.init_date = init_date
                person.save()
                
                staff = actions.add_new_staff(college, person, staff_payload)
                staff.save()
                
                if staff_payload.main_role == roles.ROLE_FACULTY:
                    actions.add_staff_subject(staff, subject, 1).save()
                
                role_param = actions.add_staff_role(college, staff, rpinfo)
                role_param.save()
                staff.main_roleparam_obj = role_param
                staff.save()
                
        except:
            # TODO: log this error
            messages.error(req, "An error occured")
        else:
            messages.success(req, "Staff added successfully")

        return utils.redirect_back(req)
        # return render(req, "sl/partials/tmp.html")
