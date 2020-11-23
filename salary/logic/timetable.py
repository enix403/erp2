from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from datetime import time as time_t
    from typing import List, Optional
    
from . import lecture as l_lecture


from ..models import (
    College, 
    TimeTable, 
    TimeTableLecture, 
    TimeTableCell,
    Section,
    RoleParam,
    Subject,
    TableActivationHistory,
)
from .constants import LectureType

import datetime



class CellInfo:
    faculty_param: RoleParam
    subject: Subject
    table_lecture: TimeTableLecture


class TableLectureSlot:
    lecture_type: int

    time_start: time_t
    time_end: time_t
    
    

def make_table(college: College, week_day: int, slots: List[TableLectureSlot]):
    table = TimeTable()
    table.week_day = week_day
    table.college = college
    table.active = 1

    table.save()

    lecture_index = 0
    ui_number = 1

    lectures_bulk = []
    
    history = TableActivationHistory()
    history.table = table
    history.date_start = datetime.date.today()
    history.current = 1
    history.table_weekday = week_day
    history.college = college
    
    history.save()
    
    for slot in slots:
        lecture = TimeTableLecture()
        lecture.time_table = table
        lecture.lecture_type = slot.lecture_type
        lecture.time_start = slot.time_start
        lecture.time_end = slot.time_end

        lecture.lecture_index = lecture_index

        if slot.lecture_type == LectureType.NORMAL:
            lecture.ui_number = ui_number
            ui_number += 1
        else:
            lecture.ui_number = 0

        lecture_index += 1

        # lecture.save()
        lectures_bulk.append(lecture)

    TimeTableLecture.objects.bulk_create(lectures_bulk)
    
    return table


def deactivate_table(college: College, table: TimeTable):
    
    today = datetime.date.today()
    l_lecture.LectureTableManager(college, today).find_date_table(today, True)
    
    history = TableActivationHistory.objects.filter(table=table, current=1, table_weekday=table.week_day).first()
    if history is not None:
        history.date_end = datetime.date.today()
        history.current = 0
        
        history.save()
    
    
    table.active = 0
    table.save()


def make_table_slots(table: TimeTable, section: Section, cells_info: List[CellInfo]):
    cells = []
    for cell_info in cells_info:
        cell = TimeTableCell()
        cell.subject = cell_info.subject
        cell.faculty_param = cell_info.faculty_param
        cell.section = section
        cell.lecture = cell_info.table_lecture
        cell.lecture_type = cell_info.table_lecture.lecture_type
        cell.time_table = table
        cell.lecture_index = cell_info.table_lecture.lecture_index
        cell.active = 1
        
        cells.append(cell)
    
    TimeTableCell.objects.bulk_create(cells)
