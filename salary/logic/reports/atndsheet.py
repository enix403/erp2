from __future__ import annotations
import datetime
from collections import defaultdict

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from typing import List, Optional, Dict
    from ...models import (
        TimeTableCell,
        Section
    )
    
# from django.db.models import Q


from base import helpers

from ...models import (
    College,
    Staff,
)

from ..holidays import HolidayManager
# from ..atnd import AttendanceManager
from .. import roles
from .. import leave_types

from ..atnd import AttendanceManager


class AtndSheetStaffRow:
    name: str
    info: str
    
    days: list
    
    def __init__(self):
        self.name = ''
        self.info = ''
        self.days = []
    
        
class AtndSheetType:
    FACULTY = 0
    STAFF = 1




def _fetch_staff(
    college: College,
    date_start: datetime.date,
    date_end: datetime.date,
    sheet_type: int
):
    
    # end_1 = Q(date_start__lte=date_start) & Q(date_end__gte=date_start)
    # end_2 = Q(date_start__lte=date_end) & Q(date_end__gte=date_end)
    # mid = Q(date_start__gte=date_start) & Q(date_end__lte=date_end)

    if sheet_type == AtndSheetType.FACULTY:
        return college.staffs.filter(
            # end_1 | end_2 | mid,
            main_role=roles.ROLE_FACULTY,
            # active=1
        )
    else:
        return college.staffs.exclude(
            main_role=roles.ROLE_FACULTY,
        )
        # ).filter(
            # end_1 | end_2 | mid,
            # active=1
        # )



def make_atnd_sheet(
    college: College,
    date_start: datetime.date,
    date_end: datetime.date,
    sheet_type: int
):
    
    atnd_manager = AttendanceManager(college, date_start, date_end)
    hm = HolidayManager(college, date_start, date_end)
    
    plus_one_day = datetime.timedelta(days=1)
    rp_queryset = _fetch_staff(college, date_start, date_end, sheet_type)
    
    if sheet_type == AtndSheetType.STAFF:
        staff_lst: List[Staff] = list(rp_queryset)
    else:
        staff_lst: List[Staff] = list(rp_queryset.prefetch_related('fac_subjects', 'fac_subjects__target_subject'))
    
    sheet_rows: Dict[int, AtndSheetStaffRow] = defaultdict(AtndSheetStaffRow)
    for rp in staff_lst:
        row = sheet_rows[rp.pk]
        row.name = rp.name
        if sheet_type == AtndSheetType.FACULTY:
            subject = helpers.get_first([s.target_subject for s in rp.fac_subjects.all() if s.main == 1])
            if subject is not None:
                row.info = subject.name
            else:
                row.info = '--Error--'
                
        else:
            row.info = roles.role_from_id(rp.main_role).name
            
    
    current = date_start
    
    
    while current <= date_end:
        is_holiday = hm.is_holiday(current)
        for r in staff_lst:
            data_row = sheet_rows[r.pk]
            
            if is_holiday:
                data_row.days.append('H')
                continue
            
            atnd_row = atnd_manager.get_staff_atnd_row(r.pk, current)
            
            if atnd_row is not None and atnd_row.leave_status == leave_types.STATUS_PRESENT:
                data_row.days.append('P')
            else:
                data_row.days.append('A')
                    
            
        current = current + plus_one_day

    return sheet_rows


"""
import salary.logic.reports.atndsheet as ra
c = College.objects.first()
import datetime
sd = datetime.date(2020, 10, 11)
ed = datetime.date.today()
a = ra.make_atnd_sheet(c, sd, ed, 0)
"""
