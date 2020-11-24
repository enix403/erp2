from __future__ import annotations
import datetime

from ..logic.constants import StaffStatus
from ..logic import roles
from django.db.models import Q

def college_active_staff(college):
    return college.staffs.filter(status=StaffStatus.ACTIVE)

def college_active_sections(college):
    return college.sections.filter(active=1)

def staff_role_suffix(staff):
    return 'F' if staff.main_role == roles.ROLE_FACULTY else 'A'

def date_range_query(
    date_start: datetime.date,
    date_end: datetime.date = None,
    date_start_label='date_start',
    date_end_label='date_end',
):

    lookup_end_gte = f'{date_end_label}__gte'
    lookup_start_lte = f'{date_start_label}__lte'

    if date_end is None or date_start == date_end:
        return Q(**{
            lookup_end_gte: date_start,
            lookup_start_lte: date_start,
        })

    lookup_start_gte = f'{date_start_label}__gte'
    lookup_end_lte = f'{date_end_label}__lte'

    end_1 = Q(**{lookup_start_lte: date_start}) & Q(**{lookup_end_gte: date_start})
    end_2 = Q(**{lookup_start_lte: date_end}) & Q(**{lookup_end_gte: date_end})
    mid = Q(**{lookup_start_gte: date_start}) & Q(**{lookup_end_lte: date_end})
    
    return end_1 | end_2 | mid

    

def fetch_date_range(
    qs_obj,
    date_start: datetime.date,
    date_end: datetime.date = None,
    date_start_label='date_start',
    date_end_label='date_end',
):
    
    return qs_obj.filter(date_range_query(date_start, date_end, date_start_label, date_end_label))
    

def loop_dates(date_start, date_end):
    current = date_start
    plus_one_day = datetime.timedelta(days=1)
    
    while current <= date_end:
        yield current
        current = current + plus_one_day
    