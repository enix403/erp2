from __future__ import annotations
# from typing import Optional, List
import json
from jsonschema import validate
# from dateutil import parser as datetime_parser

from django.views import View
from django.shortcuts import render, reverse
from django.contrib import messages
from django.http import Http404
# from django.middleware.csrf import get_token

from base import helpers, datetimeformat

from .execptions import DisplayToUserException
from ..models import (
    College,
    # TimeTable,
    # RoleParam,
    TimeTable,
    Subject,
)

from ..logic.constants import StaffStatus
# from ..logic import table as l_timetable

from ..logic.table import cellmanager
from ..logic.table.utils import parse_policy_str


from ..auth.validation import validate_college

from .. import utils


class Action_UpdateCell(View):
    
    cell_payload_schema = {
        'type': 'array',
        'items': {
            'type': 'object',
            'properties': {
                'facultyId': {'type': 'number'},
                'subjectId': {'type': 'number'},
                'ranges': {
                    'type': 'array',
                    'items': {
                        'type': 'array',
                        'items': {'type': 'number'},
                        'minItems': 2,
                        'maxItems': 2,
                    }
                }
            }
        }
    }
    
    def post(self, req):
        bag = helpers.get_bag(req)

        try:
            fragments_data = json.loads(bag.get("fragments_json", "[]"))
            validate(instance=fragments_data, schema=self.cell_payload_schema)

        except:
            raise DisplayToUserException('An error occured (ERR_INVALID_PAYLOAD)')
        
        college = College.objects.filter(pk=helpers.to_int(bag.get('college_id'))).first()
        if college is None:
            raise DisplayToUserException('An error occured (College not found)')
        
        active_days = []

        invalid = False
        
        active_staff_ids = set(utils.college_active_staff(college).values_list('id', flat=True))
        subject_ids = set(Subject.objects.values_list('id', flat=True))

        for frag in fragments_data:
            ranges = frag['ranges']
            
            if frag['facultyId'] not in active_staff_ids:
                raise DisplayToUserException('An error occured (Some of the staff not found)')
            
            if frag['subjectId'] not in subject_ids:
                raise DisplayToUserException('An error occured (Some of the subjects not found)')
            
            for start, end in ranges:

                if start > end:
                    invalid = True
                    break

                active_days.extend(range(start, end + 1))

        # check for duplicates :)
        if len(active_days) != len(set(active_days)):
            invalid = True

        if not all(d >= 1 and d <= 6 for d in active_days):
            invalid = True
            
            
        if invalid:
            raise DisplayToUserException('Invalid day range')
        

        table = TimeTable.objects.filter(pk=helpers.to_int(bag.get('table_id')), college=college).first()
        if table is None:
            raise DisplayToUserException('An error occured (Table not found)')

        section = college.sections.filter(active=1, pk=helpers.to_int(bag.get('section_id'))).first()
        if section is None:
            raise DisplayToUserException('An error occured (Section not found)')


        lecture_index = helpers.to_int(bag.get('lecture_index', None))
        if lecture_index < 0:
            raise DisplayToUserException('Invalid payload')

        # TODO: check for duplicate faculty in same lecture
        
        cellmanager.update_active_cell(table, lecture_index, section, fragments_data)
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
                        'ranges': parse_policy_str(frag.rep_policy)
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

        table = TimeTable.objects.filter(college=college, main=1).prefetch_related('lectures').first()

        server_data['table_id'] = table.pk

        # table_lectures = list(table.lectures.order_by('lecture_index'))
        table_lectures = list(table.lectures.all())
        table_lectures.sort(key=lambda l: l.lecture_index)

        data_lectures = []
        data_lecture_times = []

        time_formatter = datetimeformat.formatter(datetimeformat.TIME_UI)

        for l in table_lectures:
            data_lectures.append(l.lecture_type)
            data_lecture_times.append(time_formatter(l.time_start) + ' - ' + time_formatter(l.time_end))

        table_data = {

            'lectures': data_lectures,
            'lectureTimes': [data_lecture_times],

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
