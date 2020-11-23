from __future__ import annotations
import datetime

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from ...models import (
        Staff,
        Subject
    )



from .utils import make_policy_str

from ...models import (
    TimeTable,
    TimeTableCell,
    TimeTableCellFragment,
    LectureRecord
)

from ..lecture import get_cell_discovery


# def is_cell_discovered(date: datetime.date, lecture_index, section, cell = None):
    
#     force_discover = False
    
#     discovered = LectureRecord.objects.filter(
#         # Q(lecture_index=cell.lecture_index, section__pk=cell.section.pk) | Q(cell=cell),
#         Q(lecture_index=lecture_index, section__pk=section.pk),
#         m_date=date,
#     ).exists()
    
#     if not force_discover:
#         return discovered
    
    
#     if discovered:
#         return True
    
#     if cell is not None:
#         mark_lecture_unspec(date, cell, lecture_index, section)
#         return True
    
#     return False
    
    
        

def update_active_cell(table: TimeTable, lecture_index, section, fragments):
    old_cell: TimeTableCell = table.cells.filter(lecture_index=lecture_index, section=section, active=1).first()

    today = datetime.date.today()
    tomorrow = today + datetime.timedelta(days=1)
    cell_discovered = get_cell_discovery(today, lecture_index, section, old_cell) is not None
    
    overwrite = False

    
    if not old_cell:
        new_cell = TimeTableCell()
        if cell_discovered:
            new_cell.date_start = tomorrow
        else:
            new_cell.date_start = today
    else:
        
        old_cell.active = 0
        
        if old_cell.date_start > today:
            new_cell = old_cell
            overwrite = True
            print()
        
        elif cell_discovered:
            old_cell.date_end = today
            new_cell = TimeTableCell()
            new_cell.date_start = tomorrow
            
        else:
            if old_cell.date_start < today:
                yesterday = today - datetime.timedelta(days=1)
                old_cell.date_end = yesterday
                new_cell = TimeTableCell()
                new_cell.date_start = today
                
            else: # old_cell.date_start == today (cuz < and > have already been tested above)
                new_cell = old_cell
                overwrite = True
                
                
    
    
    new_cell.active = 1
            
    if overwrite:
        new_cell.fragments.all().delete()
        # new_cell.last = 1
    else:
        if old_cell:
            # old_cell.last = 0
            old_cell.save()
        new_cell.lecture_index = lecture_index
        new_cell.section = section
        new_cell.table = table
        
    
    if len(fragments) == 0:
        if overwrite:
            new_cell.delete()
        return
        
    new_cell.save()
    
    cell_frags = []

    for frag in fragments:
        cell_frag = TimeTableCellFragment()
        cell_frag.cell = new_cell
        cell_frag.subject_id = frag['subjectId']
        cell_frag.staff_id = frag['facultyId']
        cell_frag.rep_policy = make_policy_str(frag['ranges'])

        cell_frags.append(cell_frag)

    TimeTableCellFragment.objects.bulk_create(cell_frags)
    
    
    return new_cell

