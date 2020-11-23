from __future__ import annotations

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from ..models import (
        RoleParam,
        Staff,
    )

from django.shortcuts import render
from django.views import View


from ..logic.constants import StaffStatus

from ..models import (
    College,
)


class MainTransfersView(View):
    def get(self, req):


        college_list = []
        for c in College.objects.all():
            staff = []
            for f in c.staffs.filter(status=StaffStatus.ACTIVE): # type: Staff
                staff.append({
                    'id': f.pk,
                    'name': f.name,
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
