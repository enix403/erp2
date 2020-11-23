from __future__ import annotations
from typing import TYPE_CHECKING
import json

if TYPE_CHECKING:
    from ...models import (
        Staff,
        Subject,
        TimeTableCellFragment,
    )
    from typing import List, Dict

import datetime
# import time

from django.db.models import Q

from base import datetimeformat
from ...models import (
    TimeTable,
    TimeTableCell,
)

from .utils import parse_policy_str

class CellLectureInfo:
    
    cell: TimeTableCell = None
    # section_pk: int
    # lecture_index: int
    
    faculty: Staff = None
    subject: Subject = None
    
    @property
    def faculty_id(self):
        if self.faculty is None:
            return -1
        
        return self.faculty.pk
    
    @property
    def lecture_index(self):
        return self.cell.lecture_index
    
    
    def __str__(self):
        return "%s (%s)" % (self.faculty.name, self.subject.name)
    
    def __repr__(self):
        return self.__str__()
    
    # @classmethod
    # def make_empty(cls):
    #     return cls()


class ParsedTimeTable:
        
    date: datetime.date
    num_lectures: int
    parsed_cells: List[Dict[int, CellLectureInfo]]
    lectures: list
    
    def __init__(self, date, lectures):
        self.date = date
        self.lectures = lectures
        self.num_lectures = len(lectures)
        self.num_lectures_all = self.num_lectures
        self.parsed_cells = []
        
        for _ in range(self.num_lectures):
            self.parsed_cells.append({})
            
    def shake_empty(self):
        num_lectures = self.num_lectures_all
        for i in range(self.num_lectures_all - 1, -1, -1):
            if self.parsed_cells[i]:
               break
           
            del self.parsed_cells[i]
            num_lectures -= 1
            
            
        self.num_lectures = num_lectures
            
            
    def __getitem__(self, lecture_index):
        return self.parsed_cells[lecture_index]

    
    def all_cells(self):
        for i in range(self.num_lectures):
            for v in self.parsed_cells[i].values():
                yield v
                
                
    def section_cells(self, section_id):
        for i in range(self.num_lectures):
            cell_info = self.parsed_cells[i].get(section_id)
            if cell_info is not None:
                yield cell_info
                
from ... import utils

class TimeTableParser:
    
    @classmethod
    def parse_direct(cls, table, date):
        parser = cls(table, date)
        # st = time.time()
        res = parser.parse_date(date)
        # end = time.time()
        
        # print(end - st)
        return res
    
    def __init__(self, table: TimeTable, date_start: datetime.date, date_end: datetime.date = None):
        
        self.date_start = date_start
        self.date_end = date_end
        
        # if date_end is None or date_start == date_end:
        #     cl_queryset = table.cells.filter(
        #         date_end__gte=date_start,
        #         date_start__lte=date_start,
        #     )
        # else:
        #     end_1 = Q(date_start__lte=self.date_start) & Q(date_end__gte=self.date_start)
        #     end_2 = Q(date_start__lte=self.date_end) & Q(date_end__gte=self.date_end)
        #     mid = Q(date_start__gte=self.date_start) & Q(date_end__lte=self.date_end)

        #     cl_queryset = table.cells.filter(
        #         end_1 | end_2 | mid,
        #     )
            
        cl_queryset = utils.fetch_date_range(table.cells, date_start, date_end)
            
        self.cells = list(cl_queryset.prefetch_related('fragments', 'fragments__staff', 'fragments__subject'))
            
        self.max_lecture_count = table.lecture_count
        self.table_lectures = list(table.lectures.all())
        
        self.table_lectures.sort(key=lambda l: l.lecture_index)
        
        
        self.lecture_cells_set = []
        
        self._group_cells()
        
    def _group_cells(self):
        self.lecture_cells_set = []
        for _ in range(self.max_lecture_count):
            self.lecture_cells_set.append([])

        for cell in self.cells:  # type: TimeTableCell
            self.lecture_cells_set[cell.lecture_index].append(cell)
        
        
    @staticmethod
    def parse_cell(cell: TimeTableCell, date_weekday):
        for frag in cell.fragments.all():  # type: TimeTableCellFragment
            policy_ranges = parse_policy_str(frag.rep_policy)

            for (start, end) in policy_ranges:
                if date_weekday >= start and date_weekday <= end:
                    cell_info = CellLectureInfo()
                    cell_info.faculty = frag.staff
                    cell_info.subject = frag.subject
                    cell_info.cell = cell
                    

                    return cell_info

        return None
    
    def _is_cell_in_date(self, cell, date):
        return date >= cell.date_start and date <= cell.date_end
        
        
    def parse_date(self, date: datetime.date):
        parsed_table = ParsedTimeTable(date, self.table_lectures)
        date_weekday = int(date.strftime(datetimeformat.WEEKDAY_NUM))
        
        for lecture_index in range(self.max_lecture_count):
            for cell in self.lecture_cells_set[lecture_index]:
                if self._is_cell_in_date(cell, date):
                    cell_info = self.parse_cell(cell, date_weekday)
                    # cell_info.lecture_index = lecture_index
                    # cell_info.section_pk = cell.section_id
                    if cell_info:
                        parsed_table.parsed_cells[lecture_index][cell.section_id] = cell_info
                        
        
        parsed_table.shake_empty()
        return parsed_table

        
        


"""
import salary.logic.table.parsing as lt
import datetime
t = TimeTable.objects.first()
td = datetime.date.today()

table = lt.TimeTableParser.parse_direct(t, td)
"""
