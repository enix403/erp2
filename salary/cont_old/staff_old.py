from __future__ import annotations
from django.shortcuts import render, redirect, reverse
from django.views import View
from django.contrib import messages
from django.http import Http404
from django.db import transaction

from dateutil import parser as datetime_parser

from base import helpers
from .execptions import DisplayToUserException

from ..models import (
    College,
    Subject,
    # Person,
    Staff
)

from ..logic import college as l_college
from ..logic import roles
from ..logic import constants

from ..auth.validation import validate_college

class StaffView(View):
    def get(self, req, college_id):
        college: College = helpers.fetch_model_clean(College, college_id)
        if college == None:
            raise Http404
        
        validate_college(college)

        return render(req, "sl/pages/staff/st-main.html", {
            "college": college,
            'college_staffs': college.staffs.all().prefetch_related('role_params'),

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
        
        # TODO validate user to college

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
    def _get_role_param_info(self, bag, name, main):
        role_info = roles.role_from_id(helpers.to_int(bag.get('role')))
        subject = helpers.fetch_model_clean(Subject, bag.get('subject'))
        category = helpers.to_int(bag.get('category'))
        w_agreed = helpers.to_int(bag.get('w_agreed'))
        x_rate = helpers.to_int(bag.get('x_rate'))
        salary = helpers.to_int(bag.get('salary'))

        try:
            j_date_campus = datetime_parser.parse(bag.get('j_date_campus')).date()
        except:
            j_date_campus = None
            
        role_param_info = l_college.Impl_College.RoleParamInfo(
            name,
            role_info,
            subject,
            category,
            w_agreed,
            x_rate,
            salary,
            j_date_campus,
            main
        )
        
        return role_param_info
        
    def _validate_role_param_info(self, college, role_param_info):
        if role_param_info.role_info is None:
            raise DisplayToUserException("Invalid role")
        
        if not role_param_info.j_date_campus:
            raise DisplayToUserException("Invalid DOJ Campus")
            

        if not role_param_info.role_info.duplicate:
            if college.role_params.filter(role=role_param_info.role_info.role, active=1).exists():
                raise DisplayToUserException("A staff member with role of \"%s\" already exists" % role_param_info.role_info.name)

        if role_param_info.role_info.role == roles.ROLE_FACULTY:
            if not role_param_info.subject:
                raise DisplayToUserException("Invalid subject")

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
        
        college : College = staff.college
        validate_college(college)

        
        role_param_info = self._get_role_param_info(bag, staff.person.name, 0)
        self._validate_role_param_info(college, role_param_info)
        
        if staff.role_params.filter(role=role_param_info.role_info.role, active=1).count() > 0:
            raise DisplayToUserException('The given staff member already has a role of \"%s\"' % role_param_info.role_info.name)

        return college, staff, role_param_info    
    
    def post(self, req):
        bag = helpers.get_bag(req)
        college, staff, info = self._clean_input(bag)
        college_impl = l_college.Impl_College(college)
        
        try:
            with transaction.atomic():
                college_impl.add_staff_role(staff, info)
        except:
            messages.error(req, "An error occured")
            return helpers.redirect_back(req)
            
        else:
            messages.success(req, "Role added successfully")
            return redirect(reverse('sl_u:view-staff', args=[college.pk]))



class Action_CreateStaff(View, ValidateRoleParamMixin):
    
    def _get_param_set(self, bag):
        name = bag.get('name')
        cnic = bag.get('cnic')
        bank_acc = bag.get('bank_acc')
        gender = helpers.to_int(bag.get('gender'))
        erp_number = helpers.to_int(bag.get('erp_number'))

        try:
            j_date_kips = datetime_parser.parse(bag.get('j_date_kips')).date()
        except:
            j_date_kips = None

        param_set = l_college.Impl_College.StaffParamSet(
            name,
            cnic,
            bank_acc,
            gender,
            j_date_kips,
            erp_number
        )

        return param_set
    
    
    # coronafreequrbani.online
        
    
    def _clean_input(self, bag):  # type: QueryDict
        college: College = helpers.fetch_model_clean(College, bag.get('college_id'))
        validate_college(college)

        param_set = self._get_param_set(bag)

        fill_all = False
        if not param_set.name or not param_set.cnic or not param_set.bank_acc:
            fill_all = True
        if not param_set.j_date_kips:
            fill_all = True

        if param_set.erp_number <= 0:
            fill_all = True

        if fill_all:
            raise DisplayToUserException("Please fill all fields")

        if param_set.gender != constants.Gender.MALE and param_set.gender != constants.Gender.FEMALE:
            raise DisplayToUserException("Invalid gender")


        role_param_info = self._get_role_param_info(bag, param_set.name, 1)
        self._validate_role_param_info(college, role_param_info)

        # if Person.objects.filter(erp_number=param_set.erp_number).count() > 0:
            # raise DisplayToUserException("Duplicate ERP Number")
        
        return college, param_set, role_param_info

    def post(self, req):
        bag = helpers.get_bag(req)
        college, param_set, role_param_info = self._clean_input(bag)
        college_impl = l_college.Impl_College(college)
        
        # return helpers.redirect_back(req)
        
        
        try:
            with transaction.atomic():
                staff = college_impl.add_staff(param_set)
                college_impl.add_staff_role(staff, role_param_info)
        except:
            messages.error(req, "An error occured")
        else:
            messages.success(req, "Staff added successfully")
            

        return helpers.redirect_back(req)
