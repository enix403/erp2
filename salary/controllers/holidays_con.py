from __future__ import annotations
from typing import TYPE_CHECKING, Optional
if TYPE_CHECKING:
    from ..models import Staff

from django.shortcuts import render, get_object_or_404
from django.views import View
from django.http import HttpRequest, Http404
from django.contrib import messages

import datetime
import calendar
from dateutil import parser as datetime_parser

# from base import helpers
from base import datetimeformat, helpers
from .execptions import DisplayToUserException

# pylint: disable=unused-import
from ..models import (
    College,
    # AttendanceRow,
    Holiday
)

from ..logic import holidays as l_holidays
from ..auth.validation import validate_college


class HolidaysView(View):
    def get(self, req: HttpRequest, college_id):

        year = helpers.to_int(req.GET.get('year'), None)
        month = helpers.to_int(req.GET.get('month'), None)

        if year is None or month is None:
            td = datetime.date.today()
            year = td.year
            month = td.month

        try:
            mrange = calendar.monthrange(year, month)
            month_start = datetime.date(year=year, month=month, day=1)
            month_end = datetime.date(year=year, month=month, day=mrange[1])
        except:
            raise Http404

        college: College = get_object_or_404(College, pk=college_id)
        validate_college(college)

        hm = l_holidays.HolidayManager(college, month_start, month_end)

        rows = []
        for g in hm.get_groups():  # type: Holiday
            rows.append({
                'date_start': g.date_start.strftime(datetimeformat.DATE_UI),
                'date_end': g.date_end.strftime(datetimeformat.DATE_UI),
                'remarks': "- N/A -" if g.remarks is None else g.remarks,
                'atnd_open': "Yes" if bool(g.allow_atnd) else "No"
            })

        return render(req, "sl/pages/holidays.html", {
            'college': college,
            "month_name": month_start.strftime(datetimeformat.MONTHNAME_LONG + "-" + datetimeformat.YEAR),
            'holidays': rows
        })


class Action_AddHoliday(View):

    class Payload:
        date_start: datetime.date
        date_end: datetime.date
        allow_atnd: bool
        remarks: Optional[str]

        def __init__(self, s, e, al_atnd, rem):
            self.date_start = s
            self.date_end = e
            self.allow_atnd = al_atnd
            self.remarks = rem


    def _clean_input(self, bag):
        college: College = helpers.fetch_model_clean(College, bag.get('college_id'))
        validate_college(college)
        
        allow_atnd_str = bag.get('atnd_open')
        if allow_atnd_str == 'yes':
            allow_atnd = 1
        elif allow_atnd_str == 'no':
            allow_atnd = 0
        else:
            raise DisplayToUserException("Please specify wether attendance is open or not")
        
        remarks = bag.get('remarks')
        if remarks == '':
            remarks = None
            
        
        try:
            date_start = datetime_parser.parse(bag.get('date_start')).date()
        except:
            raise DisplayToUserException("Invalid start date")

        try:
            date_end = datetime_parser.parse(bag.get('date_end')).date()
        except:
            raise DisplayToUserException("Invalid end date")
        
        
        if date_start > date_end:
            raise DisplayToUserException("Invalid date set")
            
        
        if l_holidays.HolidayManager.overlaps(college, date_start, date_end):
            raise DisplayToUserException("Another holiday with similar dates exists")    
        
    
        payload = self.Payload(date_start, date_end, allow_atnd, remarks)
        return college, payload

    
    def post(self, req):
        bag = helpers.get_bag(req)
        college, payload = self._clean_input(bag)
        
        hl = Holiday()
        hl.remarks = payload.remarks
        hl.date_start = payload.date_start
        hl.date_end = payload.date_end
        hl.allow_atnd = payload.allow_atnd
        hl.college = college
        hl.save()
        
        messages.success(req, 'Holiday(s) added successfully')
        return helpers.redirect_back(req)