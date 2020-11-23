from __future__ import annotations
import datetime
# import time

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from ..models import (
        RoleParam,
        Staff
    )

from django.shortcuts import render, reverse
from django.views import View
from django.http import Http404, HttpResponse


from base import datetimeformat, helpers

from ..logic.reports import atndsheet as l_atndsheet
from ..logic.reports import lecturesheet as l_lecturesheet

from ..logic import roles
from ..controllers.execptions import DisplayToUserException
from ..auth.manager import AuthManager
from ..auth.validation import validate_college
from ..models import (
    College,
)

from .. import utils


class MainAdminReportsView(View):
    def get(self, req):

        user_college_pk = AuthManager.user_college_pk()

        college_list = []
        for c in College.objects.all():
            if user_college_pk == 0 or c.pk == user_college_pk:

                faculty = []
                for f in utils.college_active_staff(c).filter(has_faculty=1): #type: Staff
                    faculty.append({
                        'id': f.pk,
                        'name': f.name,
                    })

                college_list.append({
                    'id': c.pk,
                    'name': c.name,
                    'faculty': faculty
                })

        return render(req, 'sl/reports/admin/reports.html', {
            'server_data': {
                'colleges': college_list,
                'college_fixed': user_college_pk != 0,
                'urls': {
                    'atndsheet': reverse("sl_u:view-rp-atnd"),
                    'lecsheet': reverse("sl_u:view-rp-lecsheet"),
                }
            }
        })


class AtndSheetView(View):
    def get(self, req):

        bag = helpers.get_bag(req)

        college: College = College.objects.filter(pk=helpers.to_int(bag.get('college_id'))).first()
        if college is None:
            raise Http404
        validate_college(college)

        def _gen_exp(msg):
            return DisplayToUserException(user_msg=msg, route_name="sl_u:view-reports-main")

        sheet_type = helpers.to_int(bag.get('type'))
        if sheet_type != l_atndsheet.AtndSheetType.FACULTY and sheet_type != l_atndsheet.AtndSheetType.STAFF:
            raise _gen_exp("Invalid staff type")

        try:
            date_start = datetime.datetime.strptime(bag.get('from'), datetimeformat.DATE_USER_INPUT).date()
        except:
            date_start = None

        try:
            date_end = datetime.datetime.strptime(bag.get('to'), datetimeformat.DATE_USER_INPUT).date()
        except:
            date_end = None

        if date_start is None or date_end is None or date_end < date_start:
            raise _gen_exp("Invalid date range")

        sheet = l_atndsheet.make_atnd_sheet(college, date_start, date_end, sheet_type)
        day_headers = []

        current = date_start
        plus_one_day = datetime.timedelta(days=1)

        while current <= date_end:
            day_headers.append(current.strftime(datetimeformat.DAY))
            current = current + plus_one_day

        return render(req, 'sl/reports/atndsheet.html', {
            'college': college,
            'sheet_type': sheet_type,
            'AtndSheetType': l_atndsheet.AtndSheetType,
            'day_headers': day_headers,
            'sheet_rows': list(sheet.values())
        })


class LectureSheetView(View):
    def get(self, req):

        bag = helpers.get_bag(req)

        college: College = College.objects.filter(pk=helpers.to_int(bag.get('college_id'))).first()
        if college is None:
            raise Http404
        validate_college(college)

        def _gen_exp(msg):
            return DisplayToUserException(user_msg=msg, route_name="sl_u:view-reports-main")

        faculty_id = helpers.to_int(bag.get('faculty_param_id'))
        
        if faculty_id == -1:
            raise _gen_exp("NOT_IMPLEMENTED")
        
        faculty = college.staffs.filter(pk=faculty_id, has_faculty=1).first()
        if faculty is None:
            raise _gen_exp("Faculty not found")

        try:
            date_start = datetime.datetime.strptime(bag.get('from'), datetimeformat.DATE_USER_INPUT).date()
        except:
            date_start = None

        try:
            date_end = datetime.datetime.strptime(bag.get('to'), datetimeformat.DATE_USER_INPUT).date()
        except:
            date_end = None

        if date_start is None or date_end is None or date_end < date_start:
            raise _gen_exp("Invalid date range")


        # start = time.time()
        sheet = l_lecturesheet.make_lecture_sheet(college, faculty, date_start, date_end)
        # print()
        # print()
        # print()
        # print("Time Of Execution: ", time.time() - start)
        # print()
        # print()
        
        day_headers = []

        current = date_start
        plus_one_day = datetime.timedelta(days=1)

        while current <= date_end:
            day_headers.append(current.strftime(datetimeformat.DAY))
            current = current + plus_one_day

        # print(sheet.lectures[0].counts)


        return render(req, 'sl/reports/lecsheet.html', {
            'college': college,
            'faculty': faculty,
            'day_headers': day_headers,
            'lecture_sheet': sheet
        })
