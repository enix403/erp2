from __future__ import annotations

from ..models import AttendanceRow, Staff, College
import datetime
from . import leave_types
from typing import Optional, Union



class AttendancePayload:
    time_in: datetime.time
    time_out: datetime.time
    leave_status: int


class AtndUpdateResult:
    SUCCESS = 0
    ROW_LOCKED = 1
    INVALID_TIME_IN = 2
    INVALID_TIME_OUT = 3
    INVALID_LEAVE_STATUS = 4


def update_atnd(row: AttendanceRow, payload: AttendancePayload):
    is_clean = (row.leave_status == leave_types.STATUS_UNSPEC)

    if is_clean:
        if payload.leave_status == leave_types.STATUS_UNSPEC:
            return AtndUpdateResult.INVALID_LEAVE_STATUS

        row.time_in = None
        row.time_out = None
        row.rec_time_in = None
        row.rec_time_out = None

        if payload.leave_status == leave_types.STATUS_PRESENT:
            # person is present

            # check time in
            if payload.time_in == None:
                return AtndUpdateResult.INVALID_TIME_IN

            row.time_in = payload.time_in
            row.rec_time_in = datetime.datetime.now().time()
            row.leave_status = leave_types.STATUS_PRESENT
        else:
            # person is on leave
            row.leave_status = payload.leave_status
            row.rec_time_in = row.rec_time_in = datetime.datetime.now().time()

    else:
        if row.leave_status == leave_types.STATUS_PRESENT:

            # check time out
            if row.time_out == None:
                if payload.time_out == None:
                    return AtndUpdateResult.INVALID_TIME_OUT
                row.time_out = payload.time_out
                row.rec_time_out = datetime.datetime.now().time()
            else:
                # row locked
                return AtndUpdateResult.ROW_LOCKED

        else:
            # row locked
            return AtndUpdateResult.ROW_LOCKED

    row.save()
    return AtndUpdateResult.SUCCESS


class StaffAvailabilityInfo:
    available: bool
    time_start: Optional[datetime.time]
    time_end: Optional[datetime.time]

    def __init__(self, av=False, t_start=None, t_end=None):
        self.available = av
        self.time_start = t_start
        self.time_end = t_end





"""
import salary.logic.atnd as la
am = la.AttendanceManager.test()
"""

class AttendanceManager:
    
    
    @classmethod
    def test(cls):
        c = College.objects.first()
        td = datetime.date(2020, 10, 10)
        return cls(c, td, td + datetime.timedelta(days=5))
    
    
    def __init__(self, college, date_start: datetime.date, date_end: datetime.date = None):
        self.college = college
        self.date_start = date_start
        self.date_end = date_start if date_end is None else date_end

        self._db_repo = []

        if date_end is None or date_start == date_end:
           
           self._db_repo = list(AttendanceRow.objects.filter(
               college=college,
               m_date=self.date_start
            ))
            
        else:
            self._db_repo = list(AttendanceRow.objects.filter(
                college=college,
                m_date__gte=self.date_start,
                m_date__lte=self.date_end
            ))
            
    def get_staff_atnd_row(self, staff: Union[Staff, int], date: datetime.date):
        staff_id = staff.pk if isinstance(staff, Staff) else staff
        
        for row in self._db_repo:
            if row.m_date == date and row.staff_id == staff_id:
                return row
            
        return None
    
    def get_availability(self, staff: Union[Staff, int], date: datetime.date):
        atnd_row = self.get_staff_atnd_row(staff, date)
        if atnd_row is None:
            return StaffAvailabilityInfo(False)

        if atnd_row.leave_status != leave_types.STATUS_PRESENT:
            return StaffAvailabilityInfo(False)
        
        return StaffAvailabilityInfo(True, atnd_row.time_in, atnd_row.time_out)
    
    def is_staff_available(self, staff: Staff, datetime_obj: datetime.datetime):
        av_info = self.get_availability(staff, datetime_obj.date())
        if not av_info.available:
            return False
        return True or check_avinfo_range(av_info, datetime_obj.time())
            

def get_staff_atnd_row(staff: Union[Staff, int] , date: datetime.date):
    if isinstance(staff, Staff):
        return AttendanceRow.objects.filter(staff=staff, m_date=date).first()
    return AttendanceRow.objects.filter(staff_id=staff, m_date=date).first()


def get_availability(staff: Staff, date: datetime.date):
    atnd_row = get_staff_atnd_row(staff, date)
    if atnd_row is None:
        return StaffAvailabilityInfo(False)

    if atnd_row.leave_status != leave_types.STATUS_PRESENT:
        return StaffAvailabilityInfo(False)
    
    return StaffAvailabilityInfo(True, atnd_row.time_in, atnd_row.time_out)

def check_avinfo_range(info: StaffAvailabilityInfo, ch_time: datetime.time):
    
    # this should never execute cuz it would be undefined bahaviour
    # but i put it here just in case someth.....
    if info.time_start is None:
        return False
    
    if ch_time >= info.time_start:
        if info.time_end is not None:
            return ch_time <= info.time_end
        
        return True

    return False


def is_staff_available(staff: Staff, datetime_obj: datetime.datetime):
    av_info = get_availability(staff, datetime_obj.date())
    if not av_info.available:
        return False
    return check_avinfo_range(av_info, datetime_obj.time())


