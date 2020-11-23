from __future__ import annotations
from django.shortcuts import render, redirect, reverse
from django.views import View
from django.contrib import messages
from django.http import Http404
from django.db import transaction

from dateutil import parser as datetime_parser
import datetime

from base import helpers
from .execptions import DisplayToUserException

from ..models import (
    College,
    Subject,
    Person,
    Staff,
)

from ..logic import staff as l_staff
from ..logic import roles
from ..logic import constants

from ..auth.validation import validate_college


class StaffView(View):
    def get(self, req, college_id):
        college: College = helpers.fetch_model_clean(College, college_id)
        if college == None:
            raise Http404

        validate_college(college)
        
        staffs = []
        college_staffs_qs = college.staffs.filter(status=constants.StaffStatus.ACTIVE) \
            .select_related('person') \
            .prefetch_related('role_params', 'fac_subjects', 'fac_subjects__target_subject')
        for staff in college_staffs_qs: # type: Staff
            staffs.append({
                "staff_obj": staff,
                'role_param_count': staff.role_params.count(),
                'role_params': list([rp for rp in staff.role_params.all() if rp.active == 1])
            })

        return render(req, "sl/pages/staff/st-main.html", {
            "college": college,
            'college_staffs': staffs,
            
            
            'Gender': constants.Gender,
            'all_roles': roles.all_roles(),

            'subjects': Subject.objects.all(),
            'FacultyCategory': constants.FacultyCategory
        })


class AddRoleView(View):
    def get(self, req, staff_id):
        staff: Staff = Staff.objects.filter(pk=staff_id).select_related('college').first()
        if staff is None:
            raise Http404


        college = staff.college
        validate_college(college)

        return render(req, "sl/pages/staff/st-add-role.html", {
            "college": college,
            'staff': staff,

            'Gender': constants.Gender,
            'all_roles': roles.all_roles(),

            'subjects': Subject.objects.all(),
            'FacultyCategory': constants.FacultyCategory
        })


#***********************ACTIONS***********************#


class ValidateRoleParamMixin:
    def _get_role_param_info(self, bag, main, date_start):
        role_info = roles.role_from_id(helpers.to_int(bag.get('role')))
        category = helpers.to_int(bag.get('category'))
        w_agreed = helpers.to_int(bag.get('w_agreed'))
        x_rate = helpers.to_int(bag.get('x_rate'))
        salary = helpers.to_int(bag.get('salary'))

        # try:
        #     date_start = datetime_parser.parse(bag.get('transfer_date')).date()
        # except:
        #     date_start = None

        role_param_info = l_staff.RoleParamInfo(
            role_info,
            category,
            w_agreed,
            x_rate,
            salary,
            main,
            
            date_start,
            None
        )

        return role_param_info

    def _validate_role_param_info(self, college, role_param_info: l_staff.RoleParamInfo):
        if role_param_info.role_info is None:
            raise DisplayToUserException("Invalid role")


        # if not role_param_info.role_info.duplicate:
        #     if college.role_params.filter(role=role_param_info.role_info.role, active=1).exists():
        #         raise DisplayToUserException("A staff member with role of \"%s\" already exists" % role_param_info.role_info.name)

        if role_param_info.role_info.role == roles.ROLE_FACULTY:

            if not constants.FacultyCategory.is_valid(role_param_info.category):
                raise DisplayToUserException("Invalid category")

            if role_param_info.w_agreed <= 0:
                raise DisplayToUserException("Invalid workload")

            if role_param_info.x_rate <= 0:
                raise DisplayToUserException("Invalid rate")

            if role_param_info.category == constants.FacultyCategory.FAC_CATERGORY_V:
                role_param_info.salary = 0
            elif role_param_info.salary <= 0:
                raise DisplayToUserException("Invalid salary")

        elif role_param_info.salary <= 0:
            raise DisplayToUserException("Invalid salary")


class Action_AddRole(View, ValidateRoleParamMixin):
    def _clean_input(self, bag):
        staff: Staff = Staff.objects.filter(pk=helpers.to_int(bag.get('staff_id'))).select_related('college', 'person').first()
        if staff is None:
            raise DisplayToUserException('Staff not found')

        college: College = staff.college
        validate_college(college)

        role_param_info = self._get_role_param_info(bag, 0, datetime.date.today())
        self._validate_role_param_info(college, role_param_info)

        # if staff.role_params.filter(role=role_param_info.role_info.role, active=1).count() > 0:
        #     raise DisplayToUserException('The given staff member already has a role of \"%s\"' % role_param_info.role_info.name)

        return college, staff, role_param_info

    def post(self, req):
        bag = helpers.get_bag(req)
        college, staff, info = self._clean_input(bag)
        # college_impl = l_college.Impl_College(college)

        try:
            with transaction.atomic():
                
                l_staff.add_staff_role(college, staff, info)
                
        except:
            messages.error(req, "An error occured")
            return helpers.redirect_back(req)

        else:
            messages.success(req, "Role added successfully")
            return redirect(reverse('sl_u:view-staff', args=[college.pk]))


class Action_CreateStaff(View, ValidateRoleParamMixin):

    def post(self, req):
        bag = helpers.get_bag(req)
        
        college: College = College.objects.filter(pk=helpers.to_int(bag.get('college_id'))).first()
        
        if not college:
            raise DisplayToUserException("College not found")
        
        validate_college(college)

        name = bag.get('name')
        cnic = bag.get('cnic')
        bank_acc = bag.get('bank_acc')
        gender = helpers.to_int(bag.get('gender'))
        erp_number = helpers.to_int(bag.get('erp_number'))
        


        try:
            init_date = datetime_parser.parse(bag.get('init_date')).date()
        except:
            init_date = None
            
        try:
            transfer_date = datetime_parser.parse(bag.get('transfer_date')).date()
        except:
            transfer_date = None

        fill_all = False
        if not name or not cnic or not bank_acc:
            fill_all = True
        if not init_date or not transfer_date:
            fill_all = True

        if erp_number <= 0:
            fill_all = True

        if fill_all:
            raise DisplayToUserException("Please fill all fields")

        if gender != constants.Gender.MALE and gender != constants.Gender.FEMALE:
            raise DisplayToUserException("Invalid gender")
        
        
        role_param_info = self._get_role_param_info(bag, 1, transfer_date)
        self._validate_role_param_info(college, role_param_info)
        
        if role_param_info.role_info.role == roles.ROLE_FACULTY:
            subject = Subject.objects.filter(pk=helpers.to_int(bag.get('subject_id'))).first()
            if subject is None:
                raise DisplayToUserException("Invalid subject")
            
        else:
            subject = None


        # if Person.objects.filter(erp_number=param_set.erp_number).count() > 0:
        # raise DisplayToUserException("Duplicate ERP Number")

        staff_param_info = l_staff.StaffParamSet(
            transfer_date,
            role_param_info.role_info,
            subject
        )


        try:
            with transaction.atomic():
                person = Person()
                person.erp_number = erp_number
                person.name = name
                person.cnic = cnic
                person.gender = gender
                person.bank_acc = bank_acc
                person.init_date = init_date
                person.save()
                
                staff = l_staff.add_new_staff(college, person, staff_param_info)
                
                if staff_param_info.main_role.role == roles.ROLE_FACULTY:
                    l_staff.add_staff_subject(staff, staff_param_info.main_subject, 1)
                
                role_param = l_staff.add_staff_role(college, staff, role_param_info)
                staff.main_roleparam_obj = role_param
                staff.save()
                
        except:
            # raise
            messages.error(req, "An error occured")
        else:
            messages.success(req, "Staff added successfully")

        return helpers.redirect_back(req)
        # return render(req, "sl/partials/tmp.html")
