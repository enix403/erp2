from __future__ import annotations
import datetime
from typing import List

from django.db.models import Q

import base.helpers as helpers

from ..models import (
    College,
    Staff,
    RoleParam,
    # Section,
    # FacSubject,

    TimeTable,
    TimeTableCell,
    TargetTableRecord,
    TableActivationHistory,

    LectureRecord,
    Fixture,
)

from .constants import LectureRecordStatus
from . import roles
from . import atnd as l_atnd
from .constants import LectureType



def set_date_table(college: College, table: TimeTable, date: datetime.date, overwrite: bool = False):
    table_record = TargetTableRecord.objects.filter(m_date=date, college=college).first()

    if table_record is None or overwrite:
        if table_record is None:
            record = TargetTableRecord()
            record.m_date = date
            record.college = college
        else:
            record = table_record

        record.table = table
        record.save()


def set_date_table_unsafe(college: College, table: TimeTable, date: datetime.date):
    record = TargetTableRecord()
    record.college = college
    record.m_date = date
    record.table = table
    record.save()
    

class LectureTableManager:
    def __init__(self, college, date_start: datetime.date, date_end: datetime.date = None, prefetch_table_data = False):
        self.college = college
        self.date_start = date_start
        self.date_end = date_start if date_end is None else date_end
        
        self._history_repo = []
        self._records_repo = []

        hs_queryset = None
        rc_queryset = None

        if date_end is None or date_start == date_end:
            hs_queryset = TableActivationHistory.objects.filter(
                Q(date_end=None, date_start__lte=self.date_start),
                college=college,
                date_start__lte=date_start,
            )
            
            rc_queryset = TargetTableRecord.objects.filter(
                college=college,
                m_date=date_start
            )
            
        else:
            # worked this out on paper, it's kinda hard to wrap in head (a warning)
            end_1 = Q(date_start__lte=self.date_start) & Q(date_end__gte=self.date_start)
            end_2 = Q(date_start__lte=self.date_end) & Q(date_end__gte=self.date_end)
            mid = Q(date_start__gte=self.date_start) & Q(date_end__lte=self.date_end)

            hs_queryset = TableActivationHistory.objects.filter(
                Q(date_end=None, date_start__lte=self.date_end) | end_1 | end_2 | mid,
                college=college,
            ).order_by('-date_start')
            
            rc_queryset = TargetTableRecord.objects.filter(
                college=college,
                m_date__gte=self.date_start,
                m_date__lte=self.date_end
            )
            
        if prefetch_table_data:
            table_prefetch_list = [
                'table__cells', 
                # 'table__cells__faculty_param',
                # 'table__cells__section',
                'table__lectures',
            ]
                
            self._history_repo = list(hs_queryset.select_related('table').prefetch_related(*table_prefetch_list))
            self._records_repo = list(rc_queryset.select_related('table').prefetch_related(*table_prefetch_list))
        else:
            self._history_repo = list(hs_queryset.select_related('table'))
            self._records_repo = list(rc_queryset.select_related('table'))
            
                
    def find_date_table_record(self, date: datetime.date):
        for r in self._records_repo:
            if r.m_date == date:
                return r.table
            
        return None

    def find_date_table_history(self, date: datetime.date):
        weekday = int(date.strftime("%w"))
        
        fil = [h for h in self._history_repo if date >= h.date_start and h.table_weekday == weekday]
        fil.sort(key=lambda h: h.date_start)

        if len(fil) == 0:
            his = None
        else:
            his = next(reversed(fil))

        if his is None:
            return None

        if his.date_end is not None:
            if date > his.date_end:
                return None
        return his.table

    def find_date_table(self, date: datetime.date, save_record: bool = False):
        table = self.find_date_table_record(date)
        if table is not None:
            return table

        table = self.find_date_table_history(date)
        if table is None:
            return None

        if save_record:
            set_date_table_unsafe(self.college, table, date)

        return table

def calculate_given_load(param: RoleParam, table_cells: List[TimeTableCell]):
    cl = [c for c in table_cells if c.faculty_param_id == param.pk and c.lecture_type == LectureType.NORMAL]
    return len(cl)

def mark_lecture_complete(college: College, cell: TimeTableCell, date: datetime.date):
    lecture_record = LectureRecord()
    lecture_record.college = college
    lecture_record.m_date = date
    lecture_record.cell = cell
    lecture_record.status = LectureRecordStatus.COMPLETED
    lecture_record.give_penalty = 0
    lecture_record.save()


def apply_fixture(college: College, cell: TimeTableCell, staff: Staff, date: datetime.date, remarks=None):
    lecture_record = LectureRecord()
    lecture_record.college = college
    lecture_record.m_date = date
    lecture_record.cell = cell
    lecture_record.status = LectureRecordStatus.FIXED
    lecture_record.give_penalty = 1
    lecture_record.save()

    fixture = Fixture()
    fixture.m_date = date
    fixture.lecture_record = lecture_record
    fixture.cell = cell
    fixture.section = cell.section
    fixture.staff = staff
    fixture.lecture_index = cell.lecture_index
    fixture.remarks = remarks
    fixture.reason = 0
    fixture.save()

    return fixture

class FixtureSuggestion:
    def __init__(self, college: College, table: TimeTable, cell: TimeTableCell, date: datetime.date):
        self.college = college
        self.table = table
        self.cell = cell
        self.date = date
        
        self._table_cells: List[TimeTableCell] = list(table.cells.filter(active=1))
        
        self._sug_reason = None
        self._av_params = []
        self._sug_params = []
        
        
    def get_av_params(self):
        return self._av_params
    
    def get_sug_params(self):
        return self._sug_params
    
    def get_sug_reason(self):
        return self._sug_reason
    
        
    def is_empty_av(self):
        return len(self._av_params) == 0
    
    def is_empty_sug(self):
        return len(self._sug_params) == 0
        
    def process(self):
        av_params = self.fixture_av_role_params()
        self._av_params = av_params
        sug_params, reason = self.fixture_sug_role_params(av_params)
        self._sug_params = sug_params
        self._sug_reason = reason
        
    
    def fixture_av_role_params(self):

        college_role_params_all = list(
            self.college.role_params.filter(active=1).prefetch_related('fac_subjects')
        )

        role_params = []

        principle = helpers.get_first([r for r in college_role_params_all if r.role == roles.ROLE_PRINCIPLE])
        if principle is not None:
            role_params.append(principle)

        conslr = helpers.get_first([r for r in college_role_params_all if r.role == roles.ROLE_CONSELLER])
        if conslr is not None:
            role_params.append(conslr)

        lecture_cells = [c for c in self._table_cells if c.lecture_id == self.cell.lecture_id]

        lecture_fac_ids = [c.faculty_param_id for c in lecture_cells]
        lecture_cell_ids = [c.pk for c in lecture_cells]


        free_faculty = [r for r in college_role_params_all if r.pk not in lecture_fac_ids and r.role == roles.ROLE_FACULTY]
        role_params.extend(free_faculty)

        fixtures_filtered = []
        date_lecture_fixtures = list(Fixture.objects.filter(m_date=self.date, cell__pk__in=lecture_cell_ids))
        for param in role_params:
            fixture_count = 0
            for fix in date_lecture_fixtures:
                if fix.staff_id == param.staff_id:
                    fixture_count += 1

            if fixture_count > 0:
                continue

            fixtures_filtered.append(param)

        present = []
        for param in fixtures_filtered:
            info = l_atnd.get_availability(param.staff_id, self.date)
            if info.available:
                if l_atnd.check_avinfo_range(info, self.cell.lecture.time_start):
                    present.append(param)

        return present

    
    def _filter_underload(self, role_params: List[RoleParam]):
        underload = []
        for param in role_params:
            given_load = calculate_given_load(param, self._table_cells)
            if given_load < param.w_agreed:
                underload.append(param)

        return underload


    def _filter_class_teacher(self, role_params: List[RoleParam]):
        res = []
        section_pk = self.cell.section_id
        for param in role_params:
            cl = [c for c in self._table_cells if c.section_id == section_pk and c.faculty_param_id == param.pk]
            if len(cl) > 0:
                res.append(param)
        return res


    def _filter_subject(self, role_params: List[RoleParam]):
        res = []
        subject_pk = self.cell.subject_id
        for param in role_params:
            for fac_sub in param.fac_subjects.all():  # type: FacSubject
                if fac_sub.target_subject_id == subject_pk:
                    res.append(param)
                    break
        return res


    def fv2(self, role_params: List[RoleParam]):
        
        sources = [
            (self._filter_class_teacher, "Class Teacher"),
            (self._filter_underload, "Underload"),
            (self._filter_subject, "Subject"),
        ]
        
        faculty_params = [p for p in role_params if p.role == roles.ROLE_FACULTY]
        
        last_index = len(sources) - 1

        next_params = faculty_params
        for i, (func, reason) in enumerate(sources):
            current = func(next_params)
            if len(current) == 1 or i == last_index:
                return current, reason
            if len(current) != 0:
                next_params = current
            
        

    def fixture_sug_role_params(self, role_params: List[RoleParam]):
        
        return self.fv2(role_params)

        faculty_params = [p for p in role_params if p.role == roles.ROLE_FACULTY]

        next_params = faculty_params
        underload = self._filter_underload(next_params)
        if len(underload) == 1:
            return underload, "Underload"

        if len(underload) != 0:
            next_params = underload

        class_teachers = self._filter_class_teacher(next_params)
        if len(class_teachers) == 1:
            return class_teachers, "Class Teacher"

        if len(class_teachers) != 0:
            next_params = class_teachers

        subject_fl = self._filter_subject(next_params)
        return subject_fl, "Subject Teacher"
