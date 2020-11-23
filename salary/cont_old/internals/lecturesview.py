from __future__ import annotations
from typing import List
import datetime

from base import helpers, datetimeformat

from ...models import (
    TimeTable, 
    TimeTableLecture, 
    TimeTableCell, 
    LectureRecord, 
    Fixture
)
from ...logic.constants import LectureRecordStatus


class Dl_CellCompletionStatus:
    status: int
    info: str

    def __init__(self, status=None, info=None):
        self.status = status
        self.info = info


class Dl_LectureRow:
    cell_pk: int

    section_name: str
    faculty_name: str
    subject_name: str

    fixture_available: bool

    completion: Dl_CellCompletionStatus


class Dl_Lecture:
    lecture_name: str

    time_start: str
    time_end: str

    rows: List[Dl_LectureRow]
    
    def __init__(self):
        self.rows = []


def _time_to_str(val: datetime.time):
    if val == None:
        return ''

    return val.strftime("%I:%M %p")
    # return val.strftime("%H:%M")
    


def get_table_lecture_rows(
    date_lecture_records : List[LectureRecord],
    date_fixtures: List[Fixture],
    table_cells: List[TimeTableCell],
    lecture_db: TimeTableLecture,
    date: datetime.date
):
    
    lecture_cells_db = [c for c in table_cells if c.lecture_id == lecture_db.pk]

    rows = []
    for cell_db in lecture_cells_db:  # type: TimeTableCell
        row = Dl_LectureRow()
        row.cell_pk = cell_db.pk
        row.section_name = cell_db.section.name
        row.faculty_name = cell_db.faculty_param.name
        row.subject_name = cell_db.subject.name

        cell_status = Dl_CellCompletionStatus()

        record: LectureRecord = helpers.get_first([r for r in date_lecture_records if r.cell_id == cell_db.pk])
        
        row.fixture_available = True

        if record is None:
            cell_status.status = LectureRecordStatus.UNSPEC
        else:
            cell_status.status = record.status
            if record.status == LectureRecordStatus.FIXED:
                fixture = helpers.get_first([f for f in date_fixtures if f.lecture_record_id == record.pk])
                cell_status.info = fixture.staff.person.name

            row.fixture_available = False

        row.completion = cell_status
        rows.append(row)

    return rows


def make_view(table: TimeTable, date: datetime.date):
    lectures = []

    table_cells = list(table.cells.filter(active=1).select_related('section', 'faculty_param', 'subject'))
    date_lecture_records = list(LectureRecord.objects.filter(m_date=date, college_id=table.college_id))
    date_fixtures = list(Fixture.objects.filter(m_date=date).select_related('staff', 'staff__person'))
    
    time_formatter = datetimeformat.formatter(datetimeformat.TIME_UI)

    for lecture_db in table.lectures.order_by('lecture_index'):  # type: TimeTableLecture
        rows = get_table_lecture_rows(
            date_lecture_records,
            date_fixtures,
            table_cells, 
            lecture_db, 
            date
        )
        if len(rows) == 0:
            continue

        dl_lecture = Dl_Lecture()
        dl_lecture.lecture_name = lecture_db.format_name()
        dl_lecture.time_start = time_formatter(lecture_db.time_start)
        dl_lecture.time_end = time_formatter(lecture_db.time_end)
        dl_lecture.rows = rows

        lectures.append(dl_lecture)

    return lectures
