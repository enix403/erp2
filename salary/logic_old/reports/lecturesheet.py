from __future__ import annotations
import datetime
# from collections import defaultdict

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from typing import List, Optional
    from ...models import (
        TimeTableCell,
        Section
    )

from ...models import (
    College,
    RoleParam,
    Fixture,
)

from ..holidays import HolidayManager
from ..lecture import LectureTableManager, calculate_given_load
from ..constants import FacultyCategory


class LS_SectionRow:
    section: str
    counts: list
    is_null: bool
    
    def __init__(self, section_name: str):
        self.section = section_name
        self.counts = list()
        self.is_null = True
    

class LS_Meta:
    total_delivered: list
    table_lectures: list
    extra: list
    
    def __init__(self):
        # important to initialize, else each instance is going to share the same list
        self.total_delivered = []
        self.table_lectures = []
        self.extra = []
        
class LectureSheet:
    lectures: List[LS_SectionRow]
    fixtures: List[LS_SectionRow]
    meta: LS_Meta
    
    # def __init__(self):
        # self.lectures = []
        # self.fixtures = []
        
LS_HOLIDAY = 'H'
LS_ERR = 'E'



def make_lecture_sheet(
    college: College,
    faculty_param: RoleParam,
    date_start: datetime.date,
    date_end: datetime.date,
) -> Optional[LectureSheet]:
    
    
    plus_one_day = datetime.timedelta(days=1)

    sections = list(college.sections.all())
    lecture_records = list(college.lecture_records.filter(m_date__gte=date_start, m_date__lte=date_end))
    fixtures = list(Fixture.objects.filter(staff__pk=faculty_param.staff_id, m_date__gte=date_start, m_date__lte=date_end))
    
    is_visiting = (faculty_param.category == FacultyCategory.FAC_CATERGORY_V)
    # is_visiting = True
    agreed = 0 if is_visiting else faculty_param.w_agreed


    hm = HolidayManager(college, date_start, date_end)
    lm = LectureTableManager(college, date_start, date_end, True)
    
    data_lecture_rows = [None for _ in range(len(sections))]
    data_fixture_rows = [None for _ in range(len(sections))]
    meta = LS_Meta()
    
    section_indices = {}
    for i, s in enumerate(sections):
        data_lecture_rows[i] = LS_SectionRow(s.name)
        data_fixture_rows[i] = LS_SectionRow(s.name)
        section_indices[s.pk] = i

    # is_holiday = False

    current = date_start
    while current <= date_end:
        # current = current + plus_one_day
        
        is_holiday = hm.is_holiday(current)
        
        if not is_holiday:
            table = lm.find_date_table(current, False)
            is_error = table is None
        else:
            table = None
            is_error = True
            
        

        cr_lec_records = [l for l in lecture_records if l.m_date == current]
        cr_fixtures = [f for f in fixtures if f.m_date == current]

        total_delivered = 0

        for section in sections:  # type: Section
            
            index = section_indices[section.pk]
            lec_row = data_lecture_rows[index]
            fix_row = data_fixture_rows[index]
            
            if is_holiday:
                lec_row.counts.append(LS_HOLIDAY)
                fix_row.counts.append(LS_HOLIDAY)
                continue
                
            elif is_error:
                lec_row.counts.append(LS_ERR)
                fix_row.counts.append(LS_ERR)
                continue
            
            # 5477485477
            

            fs_cells_pk = [c.pk for c in table.cells.all() if c.section_id == section.pk and c.faculty_param_id == faculty_param.pk]
            record_count = len([r for r in cr_lec_records if r.cell_id in fs_cells_pk])
            fixtures_count = len([f for f in cr_fixtures if f.section_id == section.pk])
            total_delivered += record_count + fixtures_count
            
            lec_row.counts.append(record_count)
            fix_row.counts.append(fixtures_count)
            
            if record_count != 0 and lec_row.is_null:
                lec_row.is_null = False
                
            if fixtures_count != 0 and fix_row.is_null:
                fix_row.is_null = False


        if not is_holiday and not is_error:
            given_load = calculate_given_load(faculty_param, table.cells.all())
            if is_visiting:
                extra = total_delivered
            else:
                extra = total_delivered - max(min(given_load, agreed), min(total_delivered, agreed))
                
        
            meta.total_delivered.append(total_delivered)
            meta.table_lectures.append(given_load)
            meta.extra.append(extra)
        
        elif is_holiday:
            meta.total_delivered.append(LS_HOLIDAY)
            meta.table_lectures.append(LS_HOLIDAY)
            meta.extra.append(LS_HOLIDAY)
            
        elif is_error:
            meta.total_delivered.append(LS_ERR)
            meta.table_lectures.append(LS_ERR)
            meta.extra.append(LS_ERR)
        
        current = current + plus_one_day

        
        

    sheet = LectureSheet()
    sheet.lectures = data_lecture_rows
    sheet.fixtures = data_fixture_rows
    sheet.meta = meta
    
    
    return sheet
    
    
"""
from salary.logic.reports.lecturesheet import *
"""

"""

c = College.objects.first()
f = c.role_params.filter(role=1).first()
# import datetime
sd = datetime.date(2020, 10, 15)
ed = datetime.date(2020, 10, 17)
sheet = make_lecture_sheet(c, f, sd, ed)

print('Lectures')
for l in sheet.lectures:
    print(l.section, l.counts)

print()
print('Fixtures')
for f in sheet.fixtures:
    print(f.section, f.counts)
    
print()
print('Meta')
print("Total Del: ", sheet.meta.total_delivered)
print("Table Lectures: ", sheet.meta.table_lectures)
print("Extra: ", sheet.meta.extra)
    
"""
