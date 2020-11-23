from __future__ import annotations
import datetime

from ..models import (
    # College, 
    TimeTable,
    TimeTableCell,
    TimeTableCellFragment,
    # Staff_v2
)


def parse_policy_str(rep_policy: str):
    ranges = []
    for seg in rep_policy.split(","):
        try:
            parts = list(map(int, seg.split("-")))
            if len(parts) >= 2:
                ranges.append((parts[0], parts[1]))
            else:
                ranges.append((parts[0], parts[0]))
        except:
            pass

    return ranges


def make_policy_str(ranges):
    range_segments = []
    for rng in ranges:
        # range_segments.append(str(rng[0]) + '-' + str(rng[1]))
        if rng[0] == rng[1]:
            seg_str = str(rng[0])
        else:
            seg_str = str(rng[0]) + '-' + str(rng[1])
            
        range_segments.append(seg_str)
        
        
    return ','.join(range_segments)


def is_cell_discovered(cell: TimeTableCell):
    return False


def make_default_table(college):
    
    table = TimeTable.objects.filter(college=college, main=1).first()
    
    if table is not None:
        return table
    
    table = TimeTable()
    table.college = college
    table.main = 1
    
    table.save()
    
    return table



def update_active_cell(table: TimeTable, lecture_index, section, fragments):
    old_cell: TimeTableCell = table.cells.filter(lecture_index=lecture_index, section=section, active=1).first()
    
    today = datetime.date.today()
    
    if old_cell:
        old_cell.active = 0
        old_cell.date_end = today
        
        save = True
        
        if old_cell.date_start == today:
           if not is_cell_discovered(old_cell):
               save = False
               old_cell.fragments.all().delete()
               old_cell.delete()
            
        if save:
            old_cell.save()
        
   
    if len(fragments) == 0:
        return
        
    cell = TimeTableCell()
    cell.lecture_index = lecture_index
    cell.section = section
    cell.date_start = today
    cell.table = table
    cell.active = 1
    cell.save()
    
    for frag in fragments:
        cell_frag = TimeTableCellFragment()
        cell_frag.cell = cell
        cell_frag.subject_id = frag['subjectId']
        cell_frag.staff_id = frag['facultyId']
        cell_frag.rep_policy = make_policy_str(frag['ranges'])
        
        cell_frag.save()
        
    
        

    

"""
from salary.logic.timetablelogic import *
s = Section.objects.first()
c = College.objects.first()
t = make_default_table(c)
update_active_cell(t, 1, s, [])
"""

    
    
    
