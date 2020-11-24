from __future__ import annotations
# from typing import Optional, List
import datetime
from django.views import View
from django.shortcuts import render, redirect, reverse
from django.contrib import messages
from django.http import Http404

import base.helpers as helpers

from .execptions import DisplayToUserException
from ..models import (
    College,
    TimeTableCell,
    Staff
)


from .internals import lecturesview
from ..logic.constants import LectureRecordStatus

from ..logic import lecture as l_lecture
from ..logic.fixturesug import FixtureSuggestion
from ..logic.table import tablectrl
from ..logic.table.parsing import TimeTableParser

from ..auth.validation import validate_college


class LectureMainView(View):
    def get(self, req, college_id):
        college: College = College.objects.filter(pk=college_id).first()

        if college == None:
            raise Http404('Page not found')

        validate_college(college)

        today = datetime.date.today()
        # table = TimeTable.objects.filter(college=college, main=1).first()
        
        table = tablectrl.TableFinder.find_date_direct(college, today)
        lectures = lecturesview.make_view(college, table, today)

        return render(req, 'sl/pages/lecture/lec-main.html', {
            'college': college,
            'lectures': lectures,
            'LectureRecordStatus': LectureRecordStatus
        })



class Action_MarkComplete(View):
    def _clean_input(self, bag):
        college: College = helpers.fetch_model_clean(College, helpers.to_int(bag.get('college_id')))
        if college is None:
            raise DisplayToUserException("College not found")

        validate_college(college)
        
        table = tablectrl.TableFinder.find_date_direct(college, datetime.date.today())

        cell: TimeTableCell = table.cells.filter(pk=helpers.to_int(bag.get('cell_id'))).first()
        if cell is None:
            raise DisplayToUserException("Cell not found")
        
        # if cell.active != 1:
            # raise DisplayToUserException("Please try again (ERR_CELL_EXPIRED)")
        
        return college, cell
        

    def post(self, req):
        bag = helpers.get_bag(req)
        college, cell = self._clean_input(bag)
        now = datetime.datetime.now()

        res = l_lecture.mark_complete(college, cell, now.date()) 

        if res == -1:
            messages.error(req, "An error occured (ERR_CELL_EXPIRED)")
        else:
            messages.success(req, "Record Updated")
            

        return helpers.redirect_back(req)


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
        # table = cell.time_table
        
        table = tablectrl.TableFinder.find_date_direct(college, today)
        ptable = TimeTableParser.parse_direct(table, today)
        
        cell_info = ptable[cell.lecture_index].get(cell.section_id)
        
        if cell_info is None:
            raise Http404("Page not found")

        suggestions = FixtureSuggestion(college, cell.section_id, ptable, cell_info)
        suggestions.process()

        dl_av_params = []
        for param in suggestions.get_av_staff():
            dl_av_params.append({
                'id': param.pk,
                "name": f'{param.name} ({param.role_suffix})'
            })

        dl_sug_params = []
        reason = suggestions.get_sug_reason()
        for param in suggestions.get_sug_staff():
            dl_sug_params.append({
                "id": param.pk,
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

        table = tablectrl.TableFinder.find_date_direct(college, datetime.date.today())

        cell: TimeTableCell = table.cells.filter(pk=helpers.to_int(bag.get('cell_id'))).first()
        if cell is None:
            raise DisplayToUserException("Cell not found")

        # TODO: perform furthur validation (make sure fixtures for normal lectures only etc, remarks if not suggestion)

        # if cell.lecture_type != LectureType.NORMAL:
            # raise DisplayToUserException("Fixture for this lecture is not allowd")

        return college, cell, staff

    def post(self, req):
        bag = helpers.get_bag(req)
        college, cell, staff = self._clean_input(bag)
        today = datetime.date.today()

        res = l_lecture.apply_fixture(college, cell, staff, today)

        if res == -1:
            messages.error(req, "An error occured (ERR_CELL_EXPIRED)")
        else:
            messages.success(req, "Record Updated")

        # messages.success(req, "Record updated")
        
        
        return redirect(reverse('sl_u:view-lecture-today', args=[staff.college_id]))
