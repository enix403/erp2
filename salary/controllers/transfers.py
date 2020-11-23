from __future__ import annotations
import datetime

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from ..models import (
        RoleParam,
        Staff,
    )

from django.shortcuts import render, reverse
from django.views import View
from django.http import Http404, HttpResponse


from base import datetimeformat, helpers

from ..logic.reports import atndsheet as l_atndsheet
from ..logic.reports import lecturesheet as l_lecturesheet
from ..logic.constants import StaffStatus

from ..logic import roles
from ..controllers.execptions import DisplayToUserException
from ..auth.manager import AuthManager
from ..auth.validation import validate_college
from ..models import (
    College,
)


class MainTransfersView(View):
    def get(self, req):


        college_list = []
        for c in College.objects.all():
            staff = []
            for f in c.staffs.select_related('person').filter(status=StaffStatus.ACTIVE): # type: Staff
                staff.append({
                    'id': f.pk,
                    'name': f.person.name,
                })

            college_list.append({
                'id': c.pk,
                'name': c.name,
                'staffs': staff
            })

        return render(req, 'sl/pages/transfers.html', {
            'server_data': {
                'colleges': college_list,
                'urls': {
                }
            }
        })
