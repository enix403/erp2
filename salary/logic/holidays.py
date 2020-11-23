from __future__ import annotations
import datetime
from typing import Optional, List

from django.db.models import Q

from .. import utils

from ..models import (
    College,
    Holiday
)

from base import datetimeformat


class HolidayInfo:
    m_date: datetime.date
    allow_atnd: bool
    
    def __init__(self, m_date, allow_atnd):
        self.m_date = m_date
        self.allow_atnd = allow_atnd

class HolidayManager:
    
    def __init__(self, college: College, date_start: datetime.date, date_end: Optional[datetime.date] = None):
        self.college = college
        self.date_start = date_start
        self.date_end = date_start if date_end is None else date_end
        self._holidays_repo = []
        
        # hl_queryset = None
        
        # if date_end is None or date_start == date_end:
        #     hl_queryset = Holiday.objects.filter(
        #         college=college,
        #         date_start__lte=date_start,
        #         date_end__gte=date_start
        #     )
        # else:
        #     # worked this out on paper, it's kinda hard to wrap in head (a warning)
        #     end_1 = Q(date_start__lte=self.date_start) & Q(date_end__gte=self.date_start)
        #     end_2 = Q(date_start__lte=self.date_end) & Q(date_end__gte=self.date_end)
        #     mid = Q(date_start__gte=self.date_start) & Q(date_end__lte=self.date_end)
            
        #     hl_queryset = Holiday.objects.filter(
        #         end_1 | end_2 | mid,
        #         college=college,
        #     ).order_by('date_start')
        
        hl_queryset = utils.fetch_date_range(
            Holiday.objects.filter(college=college),
            date_start,
            date_end
        ).order_by('date_start')
        
        self._holidays_repo = list(hl_queryset)
        
        
        self._holidays_flattened: List[HolidayInfo] = []
        self._flattern()
        
        
        
    def _flattern(self):
        self._holidays_flattened.clear()
        current = self.date_start
        plus_day = datetime.timedelta(days=1)
        
        
        while current <= self.date_end:
            
            holiday_found = False
            # res = False
            
            for h in self._holidays_repo:
                if current >= h.date_start and current <= h.date_end:
                    self._holidays_flattened.append(HolidayInfo(current, bool(h.allow_atnd)))
                    holiday_found = True
                    # res = True
                    break
                
            # implicitly add all sundays
            if not holiday_found:
                weekday = int(current.strftime(datetimeformat.WEEKDAY_NUM))
                if weekday == 0: # if current day is sunday
                    self._holidays_flattened.append(HolidayInfo(current, False))
                    # res = True
                
            # print(current, str(res))
            
            current = current + plus_day
    
    def get_holiday(self, date):
        for h in self._holidays_flattened: # type: HolidayInfo
            if h.m_date == date:
                return h
            
        return None
    
    def get_days(self):
        return self._holidays_flattened
    
    def get_groups(self):
        return self._holidays_repo
        
    def is_holiday(self, date):
        return self.get_holiday(date) is not None
    
    
    @classmethod
    def make_quick(cls, college, date) -> Optional[HolidayInfo]:
        obj = cls(college, date)
        return obj.get_holiday(date)
        
        
    @classmethod
    def overlaps(cls, college: College, date_start: datetime.date, date_end: datetime.date):
        hm = cls(college, date_start, date_end)
        return len(hm.get_groups()) != 0
        