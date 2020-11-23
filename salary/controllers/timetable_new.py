from __future__ import annotations
# from typing import Optional, List
import json
import datetime
from dateutil import parser as datetime_parser

from django.views import View
from django.shortcuts import render, reverse, redirect
from django.contrib import messages
from django.http import Http404

import base.helpers as helpers

from .execptions import DisplayToUserException
from ..models import (
    College,
    TimeTable,
    RoleParam,
    Subject,
    # TableActivationHistory
)

from ..logic import timetable as l_timetable
from ..logic import lecture as l_lecture
from ..logic import roles
from ..logic.constants import LectureType, StaffStatus

from . import internals

from ..auth.validation import validate_college


class TimeTableMainView(View):
    def get(self, req, college_id):
        # college: College = get_object_or_404(College, pk=college_id)
        college: College = College.objects.filter(pk=college_id).first()

        if college is None:
            raise Http404
        
        validate_college(college)

        server_data = {}
        server_data['college'] = {
            'id': college.pk,
            'name': college.name
        }

        return render(req, "sl/pages/timetable/table-new.html", {
            'server_data': server_data
        })


class TimeTableAddSectionView(View):
    def get(self, req, table_id):
        bag = helpers.get_bag(req)
        section_id = helpers.to_int(bag.get('section_id'))
        context = internals.tablesectionview.make_list(table_id, section_id)
        return render(req, "sl/pages/timetable/table-section.html", context)


class Action_CreateTimeTable(View):

    def _clean_input(self, bag):
        college: College = helpers.fetch_model_clean(College, bag.get('college_id'))

        if college is None:
            raise Http404

        validate_college(college)

        week_day = helpers.to_int(bag.get('week_day'), None)

        if week_day == None:
            raise DisplayToUserException('Invalid week day')

        try:
            slots = json.loads(bag.get('slots_json', '[]'))
            if not isinstance(slots, list):
                raise Exception
        except:
            raise DisplayToUserException('Invalid slot payload')

        if len(slots) == 0:
            raise DisplayToUserException('Please provide atleast one slot')

        lecture_slots = []

        for slot_obj in sorted(slots, key=lambda s: s['order']):
            l_slot = l_timetable.TableLectureSlot()
            l_slot.lecture_type = slot_obj['l_type']
            try:
                l_slot.time_start = datetime_parser.parse(slot_obj['time_start']).time()
            except:
                l_slot.time_start = datetime.time()

            try:
                l_slot.time_end = datetime_parser.parse(slot_obj['time_end']).time()
            except:
                l_slot.time_end = datetime.time()

            lecture_slots.append(l_slot)

        return college, week_day, lecture_slots

    def post(self, req):
        bag = helpers.get_bag(req)
        college, week_day, slots = self._clean_input(bag)

        table = l_timetable.make_table(college, week_day, slots)
        today = datetime.date.today()
        l_lecture.set_date_table(college, table, today, False)

        messages.success(req, 'Time Table created successfully')
        return helpers.redirect_back(req)


class Action_DeleteTimeTable(View):

    def _clean_input(self, bag):
        table: TimeTable = TimeTable.objects.filter(pk=bag.get('table_id', 0)).prefetch_related('college').first()
        if table is None:
            raise DisplayToUserException("Table not found")

        validate_college(table.college)

        return table

    def post(self, req):
        bag = helpers.get_bag(req)
        table = self._clean_input(bag)

        l_timetable.deactivate_table(table.college, table)

        messages.success(req, "Time Table deleted successfully")
        return helpers.redirect_back(req)


class Action_AddTimeTableSection(View):

    def _clean_input(self, bag):
        college: College = helpers.fetch_model_clean(College, helpers.to_int(bag.get('college_id')))
        section = college.sections.filter(pk=helpers.to_int(bag.get('section_id')), active=1).first()
        table: TimeTable = college.time_tables.filter(pk=helpers.to_int(bag.get('table_id')), active=1).first()
        # TODO: validate

        validate_college(college)

        if table.cells.filter(section=section, active=1).exists():
            raise DisplayToUserException('Table already exists')

        try:
            lectures = json.loads(bag.get('lectures_json', '[]'))
            if not isinstance(lectures, list):
                raise Exception
        except:
            raise DisplayToUserException('Invalid lecture payload')

        lecture_cells = []
        for lecture_obj in lectures:

            lecture_id = lecture_obj['lecture_id']
            subject_id = lecture_obj['subject_id'] or 1
            fac_id = lecture_obj['faculty_param_id'] or 1

            # print(lecture_obj)

            info = l_timetable.CellInfo()

            faculty_param = RoleParam.objects.filter(pk=fac_id, role=roles.ROLE_FACULTY, active=1).prefetch_related('staff').first()

            if faculty_param is None or faculty_param.staff.status != StaffStatus.ACTIVE:
                raise DisplayToUserException('Some of the staff not found')

            subject = Subject.objects.filter(pk=subject_id).first()
            if subject is None:
                raise DisplayToUserException('Some of the subjects not found')

            if not faculty_param.fac_subjects.filter(target_subject__pk=subject.pk).exists():
                raise DisplayToUserException('Subject integrity is violated')

            info.subject = subject
            info.faculty_param = faculty_param
            info.table_lecture = table.lectures.get(pk=lecture_id)

            lecture_cells.append(info)

        return college, table, section, lecture_cells

    def post(self, req):
        bag = helpers.get_bag(req)
        college, table, section, cells_info = self._clean_input(bag)

        l_timetable.make_table_slots(table, section, cells_info)

        messages.success(req, "Section added successfully")
        return redirect(reverse('sl_u:view-timetable', args=[college.pk]))
