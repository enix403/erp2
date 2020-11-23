
from typing import List

from ...models import (
    TimeTable,
    College,
    LectureRecord,
    Fixture
)

import datetime
from base import datetimeformat, helpers

from ...logic.table.parsing import TimeTableParser, CellLectureInfo
from ...logic.constants import LectureRecordStatus, LectureType


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



# def make_dl_row(cell_info: CellLectureInfo):
#     dl_row = Dl_LectureRow()
#     dl_row.cell_pk = cell_info.cell.pk
#     dl_row.faculty_name = cell_info.faculty.name
#     dl_row.subject_name = cell_info.subject.name
#     dl_row.fixture_available = False
#     dl_row.completion = Dl_CellCompletionStatus(status=LectureRecordStatus.UNSPEC)
    
#     return dl_row
    

# def get_lecture_dl_rows(active_sections, lecture_cells):
    
#     rows = []
#     for (section_id, section_name) in active_sections:
#         cell_info: CellLectureInfo = lecture_cells.get(section_id, None)
#         if cell_info:
#             dl_row = make_dl_row(cell_info)
#             dl_row.section_name = section_name
            
#             rows.append(dl_row)

    
#     return rows


def get_lecture_dl_rows(
    active_sections,
    lecture_cells,
    date_lecture_records,
    date_fixtures
):
    rows = []
    for (section_id, section_name) in active_sections:
        cell_info: CellLectureInfo = lecture_cells.get(section_id, None)
        
        if cell_info:
            row = Dl_LectureRow()
            row.cell_pk = cell_info.cell.pk
            row.section_name = section_name
            row.faculty_name = cell_info.faculty.name
            row.subject_name = cell_info.subject.name
            
            cell_status = Dl_CellCompletionStatus()
            cell_id = cell_info.cell.pk
            
            record: LectureRecord = helpers.get_first([r for r in date_lecture_records if r.cell_id == cell_id])
            
            row.fixture_available = True

            if record is None:
                cell_status.status = LectureRecordStatus.UNSPEC
            else:
                cell_status.status = record.status
                row.fixture_available = record.status == LectureRecordStatus.UNSPEC
                
                if record.status == LectureRecordStatus.FIXED:
                    fixture = helpers.get_first([f for f in date_fixtures if f.lecture_record_id == record.pk])
                    cell_status.info = fixture.staff.name
                
                
            
            row.completion = cell_status
            rows.append(row)
                
                

    return rows

def make_view(college: College, table: TimeTable, date: datetime.date):
    lectures = []
    
    parsed_table = TimeTableParser.parse_direct(table, date)
    active_sections = list(college.sections.filter(active=1).values_list('id', 'name'))
    
    date_lecture_records = list(LectureRecord.objects.filter(m_date=date, college=college))
    date_fixtures = list(Fixture.objects.filter(m_date=date, college=college).select_related('staff'))


    time_formatter = datetimeformat.formatter(datetimeformat.TIME_UI)
    
    lecture_number = 1
    for lecture_index in range(parsed_table.num_lectures):
        lecture_db = parsed_table.lectures[lecture_index]
        lecture_cells = parsed_table.parsed_cells[lecture_index]
        
        rows = get_lecture_dl_rows(
            active_sections, 
            lecture_cells,
            date_lecture_records,
            date_fixtures
        )
        
        if lecture_db.lecture_type == LectureType.BREAK:
            lecture_name = "Break"
        else:
            lecture_name = "Lecture " + str(lecture_number)
            lecture_number += 1
        
        if len(rows) == 0:
            continue
        
        dl_lecture = Dl_Lecture()
        dl_lecture.lecture_name = lecture_name
        dl_lecture.time_start = time_formatter(lecture_db.time_start)
        dl_lecture.time_end = time_formatter(lecture_db.time_end)
        dl_lecture.rows = rows

        lectures.append(dl_lecture)
            
        
    

    return lectures
