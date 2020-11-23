from __future__ import annotations
# from typing import Optional, List
import json
# import datetime
# from dateutil import parser as datetime_parser

from django.views import View
from django.shortcuts import render, reverse
from django.contrib import messages
from django.http import Http404
# from django.middleware.csrf import get_token

import base.helpers as helpers

# from .execptions import DisplayToUserException
from ..models import (
    College,
    # TimeTable,
    # RoleParam,
    TimeTable,
    Subject,
)

from ..logic.constants import StaffStatus
from ..logic import timetable as l_timetable
# from ..logic import roles

from ..auth.validation import validate_college


class Action_UpdateCell(View):
    def post(self, req):
        bag = helpers.get_bag(req)
        
        fragments_data = json.loads(bag.get("fragments_json", "[]"))
        college = College.objects.filter(pk=helpers.to_int(bag.get('college_id'))).first()
        table = TimeTable.objects.filter(pk=helpers.to_int(bag.get('table_id')), college=college).first()
        
        lecture_index = helpers.to_int(bag.get('lecture_index', None))
        section = college.sections.filter(active=1, pk=helpers.to_int(bag.get('section_id'))).first()
    
        l_timetable.update_active_cell(table, lecture_index, section, fragments_data)
        
        messages.success(req, 'Cell Updated')
        return helpers.redirect_back(req)


def make_table_data(table, college):
    table_sections = []

    table_cells = list(table.cells.filter(active=1).prefetch_related('fragments'))

    for section in college.sections.filter(active=1):

        section_cells = []
        for cell in table_cells:
            if cell.section_id == section.pk:

                cell_fragments = []
                for frag in cell.fragments.all():
                    cell_fragments.append({
                        'facultyId': frag.staff_id,
                        'subjectId': frag.subject_id,
                        'ranges': l_timetable.parse_policy_str(frag.rep_policy)
                    })

                section_cells.append({
                    'lectureIndex': cell.lecture_index,
                    'fragments': cell_fragments
                })

        table_sections.append({
            'id': section.pk,
            'name': section.name,
            'cells': section_cells
        })

    return table_sections


class TimeTableMainView(View):
    def get(self, req, college_id):
        
        
        # college: College = get_object_or_404(College, pk=college_id)
        college: College = College.objects.filter(pk=college_id).first()

        if college is None:
            raise Http404

        validate_college(college)

        server_data = {
            # 'token': get_token(req),
            'staffs': [],
            'subjects': [],
            'urls': {
                'update_cell': reverse("sl_u:update-cell")
            }
        }

        all_subjects = Subject.objects.all()

        for subject in all_subjects:
            server_data['subjects'].append({
                'id': subject.pk,
                'name': subject.name
            })

        server_data['college'] = {
            'id': college.pk,
            'name': college.name,
        }

        table = l_timetable.make_default_table(college)

        server_data['table_id'] = table.pk

        table_data = {
            'lectures': [0, 0, 0, 1, 0, 0, 0],
            'lectureTimes': [[
                '12:00 AM - 12:00 AM',
                '12:00 AM - 12:00 AM',
                '12:43 AM - 12:00 AM',
                '12:00 AM - 12:00 AM',
                '12:00 AM - 12:00 AM',
                '12:00 AM - 12:00 AM',
                '12:00 AM - 12:00 AM',
            ]],

            'sections': make_table_data(table, college)
        }

        active_staffs = list(college.staffs.filter(status=StaffStatus.ACTIVE, has_faculty=1))

        for staff in active_staffs:
            server_data['staffs'].append({
                'id': staff.pk,
                'name': staff.name,
                'allowedSubjects': list(map(lambda x: x.pk, all_subjects))
            })

        server_data['table_data'] = table_data

        return render(req, "sl/pages/timetable/table-new.html", {
            'server_data': server_data
        })
