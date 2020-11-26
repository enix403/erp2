from __future__ import annotations
import datetime
# from typing import TYPE_CHECKING

# if TYPE_CHECKING:
    # from ...models import (
        # Staff,
        # Subject
    # )
    
from django.db.models import Q

from ..constants import LectureType
from ... import utils

from ...models import (
    TimeTable,
    College,
    TimeTableLecture,
    TimeTableLectureSet
)

def _make_lec(index):
    lec = TimeTableLecture()
    lec.lecture_index = index
    lec.time_start = datetime.time(9, 30)
    lec.time_end = datetime.time(10, 25)
    lec.lecture_type = LectureType.NORMAL
    lec.active = 1
    
    return lec

def make_active_table(college):

    table = TimeTable()
    table.college = college
    table.main = 1

    
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
    
    # table.lecture_count = len(lectures)
    table.save()
    
    lectureset = TimeTableLectureSet()
    lectureset.date_start = datetime.date.today()
    lectureset.active = 1
    lectureset.table = table
    lectureset.code = 'l001000l'
    
    lectureset.save()
    
    for l in lectures:
        l.table = table
        l.lectureset = lectureset
        
    TimeTableLecture.objects.bulk_create(lectures)

    return table


class TableFinder:
    
    @classmethod
    def get_main_table(cls, college):
        table = TimeTable.objects.filter(college=college, main=1).first()
        if table is None:
            return make_active_table(college)
        
        return table
    
    
    @classmethod
    def find_date_direct(cls, college, date):
        finder = cls(college, date)
        return finder.find_date_table(date)
    
    def __init__(self, college: College, date_start, date_end = None):
        date_query = utils.date_range_query(date_start, date_end)
        
        self.tables = list(college.time_tables.filter(Q(main=1) | date_query))
        self.main_table = None
        
        for table in self.tables: # type: TimeTable
            if table.main == 1:
                self.main_table = table
                break
            
        if self.main_table is None:
            # pass
            self.main_table = make_active_table(college)
                
        
    def find_date_table(self, date):
        for table in self.tables:
            if table.main != 1 and date >= table.date_start and date <= table.date_end:
                return table
            
        return self.main_table
