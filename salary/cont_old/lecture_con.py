from __future__ import annotations
# from typing import Optional, List
import datetime
from django.views import View
from django.shortcuts import render
from django.shortcuts import reverse, redirect
from django.contrib import messages
from django.http import Http404

import base.helpers as helpers

from .execptions import DisplayToUserException
from ..models import (
    College,
    TimeTableCell,
    Staff,
    # Fixture,
    # LectureRecord
)


from ..logic import lecture as l_lecture
from ..logic import atnd as l_atnd
from .internals import lecturesview
from ..logic.constants import LectureRecordStatus, LectureType

from ..auth.validation import validate_college


class LectureMainView(View):
    def get(self, req, college_id):
        college: College = College.objects.filter(pk=college_id).first()

        if college == None:
            raise Http404('Page not found')
        
        validate_college(college)
        
        today = datetime.date.today()
        table = l_lecture.LectureTableManager(college, today).find_date_table(today, True)

        
        lectures = []
        if table is not None:
            lectures = lecturesview.make_view(table, today)
        
        return render(req, 'sl/pages/lecture/lec-main.html', {
            'college': college,
            'lectures': lectures,
            'LectureRecordStatus': LectureRecordStatus
        })
        
class ApplyFixtureView(View):
    def get(self, req, college_id, cell_id):
        college: College = helpers.fetch_model_clean(College, college_id)
        if college is None:
            raise Http404("Page not found")
        
        validate_college(college)

            
        cell: TimeTableCell = TimeTableCell.objects.filter(pk=cell_id).first()
        if cell is None:
            raise Http404("Page not found")
        
        today = datetime.date.today()
        table = cell.time_table
        
        
        suggestions = l_lecture.FixtureSuggestion(college, table, cell, today)
        suggestions.process()
     
        dl_av_params = []
        for param in suggestions.get_av_params():
            dl_av_params.append({
                'id': param.staff_id,
                "name": param.name
            })

     
        dl_sug_params = []
        reason = suggestions.get_sug_reason()
        for param in suggestions.get_sug_params():
            dl_sug_params.append({
                "id": param.staff_id,
                'name': param.name,
                "suggest_reason": reason
            })
            
       
        return render(req, 'sl/pages/lecture/lec-fixture.html', {
            'college': college,
            'cell': cell,
            'available_staff': dl_av_params,
            'suggested_staff': dl_sug_params,
        })



class Action_ApplyFixture(View):
    def _clean_input(self, bag):
        college: College = helpers.fetch_model_clean(College, bag.get('college_id'))
        if college is None:
            raise DisplayToUserException("College not found")
        
        validate_college(college)

        
        staff: Staff = college.staffs.filter(pk=helpers.to_int(bag.get('staff_id'))).first()
        if staff is None:
            raise DisplayToUserException("Staff not found")
        
        cell_id = helpers.to_int(bag.get('cell_id'))

        # cell: TimeTableCell = TimeTableCell.objects.filter(pk=cell_id).prefetch_related('time_table__cells').first()
        cell: TimeTableCell = TimeTableCell.objects.filter(pk=cell_id).select_related('time_table').first()
        if cell is None:
            raise DisplayToUserException("Cell not found")
        
        table = cell.time_table
        if table.college_id != college.pk:
            raise DisplayToUserException("Access Denied")
        

        # TODO: perform furthur validation (fixtures for normal lectures only etc, remarks if not suggestion)
        
        if cell.lecture_type != LectureType.NORMAL:
            raise DisplayToUserException("Fixture for this lecture is not allowd")
        
        return college, cell, staff
        
    def post(self, req):
        bag = helpers.get_bag(req)
        college, cell, staff = self._clean_input(bag)
        today = datetime.date.today()

        l_lecture.apply_fixture(college, cell, staff, today)
        
        messages.success(req, "Record updated")
        return redirect(reverse('sl_u:view-lecture-today', args=[staff.college_id]))




class Action_MarkComplete(View):
    # TODO: must vaidate user input
    #! right now it is totally insecure
    def _clean_input(self, bag):
        college: College = helpers.fetch_model_clean(College, helpers.to_int(bag.get('college_id')))
        if college is None:
            raise DisplayToUserException("College not found")
        
        validate_college(college)
        
        cell: TimeTableCell = TimeTableCell.objects.select_related('faculty_param').filter(pk=helpers.to_int(bag.get('cell_id'))).first()
        if cell is None:
            raise DisplayToUserException("Invalid cell")


        return college, cell
    
    def post(self, req):
        bag = helpers.get_bag(req)
        college, cell = self._clean_input(bag)
        # today = datetime.date.today()
        now = datetime.datetime.now()
        
        if not l_atnd.is_staff_available(cell.faculty_param.staff_id, now):
            raise DisplayToUserException("Requested staff is not present")
        
        l_lecture.mark_lecture_complete(college, cell, now.date())
        
        messages.success(req, "Success")
        return helpers.redirect_back(req)

        
