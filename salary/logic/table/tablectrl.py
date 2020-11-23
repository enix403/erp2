from __future__ import annotations
import datetime
# from typing import TYPE_CHECKING

# if TYPE_CHECKING:
    # from ...models import (
        # Staff,
        # Subject
    # )
    

from ..constants import LectureType

from ...models import (
    TimeTable,
    TimeTableLecture
)

def _make_lec(index):
    lec = TimeTableLecture()
    lec.lecture_index = index
    lec.time_start = datetime.time(9, 30)
    lec.time_end = datetime.time(10, 25)
    lec.lecture_type = LectureType.NORMAL
    
    return lec

def active_table(college):

    table = TimeTable.objects.filter(college=college, main=1).prefetch_related('lectures').first()

    if table is not None:
        return table

    table = TimeTable()
    table.college = college
    table.main = 1
    
    table.save()
    
    
    lectures = []
    lectures.extend([
        _make_lec(0),
        _make_lec(1),
    ])

    brk = _make_lec(2)
    brk.lecture_type = LectureType.BREAK
    lectures.append(brk)
    
    lectures.extend([
        _make_lec(3),
        _make_lec(4),
        _make_lec(5),
    ])
    
    table.lecture_count = len(lectures)
    table.save()
    
    for l in lectures:
        l.table = table
        
    TimeTableLecture.objects.bulk_create(lectures)
        

    return table



def find_current_table(college, date: datetime.date):
    return active_table(college)
