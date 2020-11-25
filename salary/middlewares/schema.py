from .internals import RouteGroup, ViewDef
from .runner import MiddlewareContext
from django.http import HttpRequest
from django.shortcuts import redirect, reverse

from ..models import AppUser
from ..auth.manager import AuthManager
from ..auth.execptions import HttpUnauthorized



def check_type_wrap(*types):
    def check_type(get_next):
        def _mid(ctx: MiddlewareContext[HttpRequest]):
        
            if AuthManager.is_type(*types):
                return get_next(ctx)
            
            raise HttpUnauthorized

        return _mid
    return check_type

def check_auth(get_next):
    def _mid(ctx: MiddlewareContext[HttpRequest]):
        user: AppUser = AuthManager.get_logged_in_user()
        if user is not None:
            if user.invalidate == 0:
                return get_next(ctx)

        return redirect(reverse('sl_u:login'))

    return _mid


route_schema = RouteGroup(
    middlewares=[
        check_auth,
    ],
    children=[
        
        ViewDef('index'),
        
        RouteGroup(
            middlewares=[
                check_type_wrap(0)
            ], 
            children=[
                ViewDef('manage'),
                ViewDef('add-station'),
                ViewDef('add-college'),
                
            ]
        ),
        
        ViewDef('view-sections'),
        ViewDef('add-regular-section'),
        ViewDef('add-merged-section'),
        
        ViewDef('view-staff'),
        ViewDef('view-add-role'),
        ViewDef('add-staff'),
        ViewDef('add-staff-role'),
        
        ViewDef('today-atnd'),
        ViewDef('update-atnd'),
        
        ViewDef('view-timetable'),
        ViewDef('view-add-section-table'),
        ViewDef('add-table'),
        ViewDef('delete-table'),
        ViewDef('table-add-section'),
        
        ViewDef('view-lecture-today'),
        ViewDef('view-apply-fix'),
        ViewDef('mark-lec'),
        
        ViewDef('view-holidays'),
        ViewDef('add-holidays'),
        
        ViewDef('view-reports-main'),
        ViewDef('view-rp-atnd'),
        ViewDef('view-rp-lecsheet'),
        
        
        ViewDef('view-create-acc'),
        ViewDef('add-user'),
        
        
        ViewDef('view-transfers'),

        
    ]
)
