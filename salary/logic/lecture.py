from __future__ import annotations
import datetime

from django.db.models import Q


from ..models import (
    TimeTableCell,
    College,
    LectureRecord,
    Section,
    Staff,
    Fixture
)

from .constants import LectureRecordStatus, LectureType
from .table.parsing import ParsedTimeTable

def calculate_given_load(ptable: ParsedTimeTable, staff_id):
    load = 0
    for lecture_index in range(ptable.num_lectures):
        lecture_type = ptable.lecture_types[lecture_index]
        if lecture_type != LectureType.NORMAL:
            continue

        for cell_info in ptable[lecture_index].values():
            if cell_info.faculty.pk == staff_id:
                load += 1

    return load

def mark_lecture_unspec(date: datetime.date, cell: TimeTableCell, section: Section):
    lecture_record = LectureRecord()
    lecture_record.college_id = section.college_id
    lecture_record.m_date = date
    lecture_record.cell = cell
    lecture_record.status = LectureRecordStatus.UNSPEC
    lecture_record.score = 0

    lecture_record.section_id = cell.section_id
    lecture_record.lecture_index = cell.lecture_index

    lecture_record.save()

    return lecture_record


def get_cell_discovery(date: datetime.date, lecture_index, section, cell=None, force_discover=None):

    if force_discover is None:
        # then fetch is from user settings
        # right now hard coded :)
        force_discover = False

    record = LectureRecord.objects.filter(
        # Q(lecture_index=cell.lecture_index, section__pk=cell.section.pk) | Q(cell=cell),
        Q(lecture_index=lecture_index, section__pk=section.pk),
        m_date=date,
    ).first()

    # have a good time understanding this if statement
    # [ hint: see the code below :) ]
    if not force_discover or record is not None or cell is None:
        return record

    return mark_lecture_unspec(date, cell, section)

    # if not force_discover:
    #     return record

    # if record is not None:
    #     return record

    # if cell is not None:
    #     return mark_lecture_unspec(date, cell, lecture_index, section)

    # return record
    
    
def mark_complete(college: College, cell: TimeTableCell, date: datetime.date):

    prev_record = get_cell_discovery(date, cell.lecture_index, cell.section, cell, False)
    
    if prev_record is None:
        
        lecture_record = LectureRecord()
        lecture_record.college = college
        lecture_record.m_date = date
        lecture_record.cell = cell
        
        lecture_record.section_id = cell.section_id
        lecture_record.lecture_index = cell.lecture_index
    else:
        
        if prev_record.status != LectureRecordStatus.UNSPEC:
            return -1
        
        lecture_record = prev_record
        
        
    lecture_record.status = LectureRecordStatus.COMPLETED
    lecture_record.score = 1

    lecture_record.save()

    return lecture_record


def apply_fixture(college: College, cell: TimeTableCell, staff: Staff, date: datetime.date, remarks=None):
    
    prev_record = get_cell_discovery(date, cell.lecture_index, cell.section, cell, False)

    if prev_record is None:

        lecture_record = LectureRecord()
        lecture_record.college = college
        lecture_record.m_date = date
        lecture_record.cell = cell

        lecture_record.section_id = cell.section_id
        lecture_record.lecture_index = cell.lecture_index
    else:
        if prev_record.status != LectureRecordStatus.UNSPEC:
            return -1

        lecture_record = prev_record
    
    lecture_record.status = LectureRecordStatus.FIXED
    lecture_record.score = -1
    lecture_record.save()

    fixture = Fixture()
    fixture.college = college
    fixture.m_date = date
    fixture.lecture_record = lecture_record
    # fixture.cell = cell
    fixture.section = cell.section
    fixture.staff = staff
    fixture.lecture_index = cell.lecture_index
    fixture.remarks = remarks
    fixture.reason = 0
    fixture.save()

    return fixture
