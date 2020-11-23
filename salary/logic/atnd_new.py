from __future__ import annotations
import datetime

from typing import Optional, Union

from ..models import (
    College,
    AttendanceRow,
    Staff
)

from ..logic import leave_types


class StaffAvailabilityInfo:
    available: bool
    time_start: Optional[datetime.time]
    time_end: Optional[datetime.time]

    def __init__(self, av=False, t_start=None, t_end=None):
        self.available = av
        self.time_start = t_start
        self.time_end = t_end


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




class AttendanceManager:

    def __init__(self, college: Union[College, int], date_start: datetime.date, date_end: datetime.date = None):
        if isinstance(college, College):
            college_id = college.pk
        else:
            college_id = college
        
        self.date_start = date_start
        self.date_end = date_start if date_end is None else date_end

        self._db_repo = []

        if date_end is None or date_start == date_end:

           self._db_repo = list(AttendanceRow.objects.filter(
               college__pk=college_id,
               m_date=self.date_start
           ))

        else:
            self._db_repo = list(AttendanceRow.objects.filter(
                college__pk=college_id,
                m_date__gte=self.date_start,
                m_date__lte=self.date_end
            ))

    def get_staff_atnd_row(self, staff_id: int, date: datetime.date):
        for row in self._db_repo:
            if row.m_date == date and row.staff_id == staff_id:
                return row

        return None

    def get_availability(self, staff: Staff, date: datetime.date):
        atnd_row = self.get_staff_atnd_row(staff.pk, date)
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


# def get_staff_atnd_row(staff: Union[Staff, int], date: datetime.date):
#     if isinstance(staff, Staff):
#         return AttendanceRow.objects.filter(staff=staff, m_date=date).first()
#     return AttendanceRow.objects.filter(staff_id=staff, m_date=date).first()


# def get_availability(staff: Staff, date: datetime.date):
#     atnd_row = get_staff_atnd_row(staff, date)
#     if atnd_row is None:
#         return StaffAvailabilityInfo(False)

#     if atnd_row.leave_status != leave_types.STATUS_PRESENT:
#         return StaffAvailabilityInfo(False)

#     return StaffAvailabilityInfo(True, atnd_row.time_in, atnd_row.time_out)


# def check_avinfo_range(info: StaffAvailabilityInfo, ch_time: datetime.time):

#     # this should never execute cuz it would be undefined bahaviour
#     # but i put it here just in case someth.....
#     if info.time_start is None:
#         return False

#     if ch_time >= info.time_start:
#         if info.time_end is not None:
#             return ch_time <= info.time_end

#         return True

#     return False


# def is_staff_available(staff: Staff, datetime_obj: datetime.datetime):
#     av_info = get_availability(staff, datetime_obj.date())
#     if not av_info.available:
#         return False
#     return True or check_avinfo_range(av_info, datetime_obj.time())
