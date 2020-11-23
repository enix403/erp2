from __future__ import annotations
# from typing import Optional, List

import base.helpers as helpers

from ...models import College, TimeTable, RoleParam, Subject, Section, TimeTableLecture

from ...logic import roles
from ...logic.constants import LectureType, StaffStatus


def make_list(table_id, section_id):

    section: Section = Section.objects.filter(pk=section_id, active=1).first()
    college: College = section.college
    table: TimeTable = college.time_tables.filter(pk=table_id, active=1).first()

    facs = []

    params_all = college.role_params.filter(role=roles.ROLE_FACULTY, active=1) \
        .select_related('staff') \
        .prefetch_related('fac_subjects', 'fac_subjects__target_subject')
    
    
    params = []
    for p in params_all:
        if p.staff.status == StaffStatus.ACTIVE:
            params.append(p)
    

    for f in params:  # type: RoleParam
        
        f_slist = ", ".join([ s.target_subject.name for s in f.fac_subjects.all() ])
        
        f_a = {
            'pk': f.pk,
            'name': f.name,
            "subject_list": f_slist
        }
        facs.append(f_a)

    infos = []
    for lecture in table.lectures.order_by('lecture_index'):  # type: TimeTableLecture
        info = {
            'pk': lecture.pk,
            'lecture_index': lecture.lecture_index,
            'lecture_name': lecture.format_name(),
            'dl_suffix': 'n_%d' % lecture.lecture_index,
            'default_null': lecture.lecture_type != LectureType.NORMAL
        }

        infos.append(info)

    context = {

        'college': college,
        'section': section,
        'table': table,

        'day_name': 'Monday',
        'facs': facs,

        'subjects': list(Subject.objects.all()),

        'lecture_infos': infos
    }

    return context
