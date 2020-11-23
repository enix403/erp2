from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from ..models import Staff

from django.shortcuts import render, get_object_or_404
from django.views import View
from django.contrib import messages

import datetime
from dateutil import parser as datetime_parser

from base import helpers
from .execptions import DisplayToUserException

from ..models import (
    College,
    AttendanceRow,
)

from ..logic import leave_types
from ..logic import atnd as l_atnd
from ..logic import holidays as l_holidays

from ..auth.validation import validate_college



class AttendanceDisplayRow:
    staff_id: int
    staff_name: str
    time_in: datetime.time
    time_out: datetime.time
    
    time_in_locked: bool
    time_out_locked: bool
    leave_locked: bool
    
    available_leaves: list
    
def time_to_str(val: datetime.time):
    if val == None:
        return ''
    
    return val.strftime("%H:%M")


def _get_available_leaves(staff: Staff, atnd_row: AttendanceRow):
    leaves = []
    staff_leave_info = leave_types.leave_from_id(None if atnd_row == None else atnd_row.leave_status)
    
    for l in leave_types.get_all_leaves():
        leaves.append({
            'id': l.id,
            'name': l.name,
            'current': staff_leave_info.id == l.id
        })
    
    return leaves


def _generate_atnd_rows(college: College, date_obj: datetime.date):
    atnd_rows = []
    
    staff_rows_db = list(AttendanceRow.objects.filter(m_date=date_obj, latest=1))
    
    for staff in college.staffs.select_related('person').all():  # type: Staff
        staff_row = helpers.get_first([r for r in staff_rows_db if r.staff_id == staff.pk])

        atnd_display_row = AttendanceDisplayRow()
        atnd_display_row.staff_id = staff.id
        atnd_display_row.staff_name = staff.person.name
        if staff_row == None:
            atnd_display_row.time_in = ''
            atnd_display_row.time_out = ''
            atnd_display_row.time_in_locked = False
            atnd_display_row.time_out_locked = True
            atnd_display_row.leave_locked = False

            
        else:
            atnd_display_row.time_in = time_to_str(staff_row.time_in)
            atnd_display_row.time_out = time_to_str(staff_row.time_out)
            atnd_display_row.time_in_locked = True
            atnd_display_row.time_out_locked = ((staff_row.time_out != None) or (staff_row.leave_status != leave_types.STATUS_PRESENT))
            atnd_display_row.leave_locked = True

        atnd_display_row.available_leaves = _get_available_leaves(staff, staff_row)
        
        atnd_rows.append(atnd_display_row)
        
    return atnd_rows


def is_atnd_open(college, date):
    holiday = l_holidays.HolidayManager.make_quick(college, date)
    if holiday is None:
        return True
    else:
        return holiday.allow_atnd


class AttendanceView(View):
    def get(self, req, college_id):
        college: College = get_object_or_404(College, pk=college_id)
        validate_college(college)

        
        td = datetime.date.today()
        rows = []
        is_open = is_atnd_open(college, td)

        if is_open:
            rows = _generate_atnd_rows(college, td)

        return render(req, "sl/pages/atnd.html", {
            'college': college,
            'atnd_rows': rows,
            'is_closed': not is_open,
        })
        


class Action_UpdateAtnd(View):
    
    response_msgs = {
        l_atnd.AtndUpdateResult.INVALID_LEAVE_STATUS: (messages.ERROR, 'Invalid attendance status'),
        l_atnd.AtndUpdateResult.INVALID_TIME_IN: (messages.ERROR, 'Invalid time-in'),
        l_atnd.AtndUpdateResult.INVALID_TIME_OUT: (messages.ERROR, 'Invalid time-out'),
        
        l_atnd.AtndUpdateResult.ROW_LOCKED: (messages.WARNING, 'Row is locked. No changes made'),
        l_atnd.AtndUpdateResult.SUCCESS: (messages.SUCCESS, 'Record updated')
    }
    
    def _get_payload(self, bag):
        
        time_in = bag.get('time_in')
        time_out = bag.get('time_out')
        leave_status = helpers.to_int(bag.get('leave_status', leave_types.STATUS_UNSPEC))

        if not leave_types.is_leave_valid(leave_status):
            raise DisplayToUserException("Invalid attendance status")

        payload = l_atnd.AttendancePayload()
        payload.leave_status = leave_status
        
        try:
            payload.time_in = datetime_parser.parse(time_in)
        except:
            payload.time_in = None
            
        try:
            payload.time_out = datetime_parser.parse(time_out)
        except:
            payload.time_out = None

        return payload

    def _clean_input(self, bag):  # type: QueryDict
        college: College = helpers.fetch_model_clean(College, bag.get('college_id'))
        
        if college is None:
            raise DisplayToUserException('College not found')
        
        validate_college(college)
        
        staff: Staff = college.staffs.filter(pk=bag.get('staff_id')).first()

        # TODO: perform validation
        payload = self._get_payload(bag)

        return college, staff, payload

    def post(self, req):
        bag = helpers.get_bag(req)
        college, staff, payload = self._clean_input(bag)
        
        # TODO: validate staff is from given college
        
        today = datetime.date.today()
        
        if not is_atnd_open(college, today):
            raise DisplayToUserException("Attendance is not open for this day")
        
        
        staff_row = AttendanceRow.objects.filter(m_date=today, staff=staff).first()
        if staff_row == None:
            staff_row = AttendanceRow()
            staff_row.leave_status = leave_types.STATUS_UNSPEC
            staff_row.m_date = today
            staff_row.college = college
            staff_row.staff = staff
            staff_row.latest = 1
            staff_row.replaces_row_id = 0
        
        result = l_atnd.update_atnd(staff_row, payload)
        
        level, msg = self.response_msgs.get(result)
        messages.add_message(req, level, msg)
        return helpers.redirect_back(req)
