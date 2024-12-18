from django.urls import path, register_converter
from django.shortcuts import redirect, reverse, render

from . import controllers
from .auth.manager import AuthManager

def root(req):
    if AuthManager.is_type(0):
        return redirect('sl_u:manage')
    return redirect(reverse('sl_u:view-staff', args=[AuthManager.user_college_pk()]))

    

# class FourDigitYearConverter:
#     regex = '[0-9]{4}'

#     def to_python(self, value):
#         return int(value)

#     def to_url(self, value):
#         return '%04d' % value
    

# class TwoDigitMonthConverter:
#     regex = '[0-9]{2}'

#     def to_python(self, value):
#         month = int(value)
#         if month < 1 or month > 12:
#             raise ValueError
        
#         return month

#     def to_url(self, value):
#         try:
#             num = int(value)
#         except:
#             num = 0
            
#         if num < 1 or num > 12:
#             raise ValueError
        
#         return '%02d' % value
    

# register_converter(FourDigitYearConverter, 'yyyy')
# register_converter(TwoDigitMonthConverter, 'mm')

# def newbase(req):
    # return render(req, 'sl/basev.html')


app_name = "sl_u"
urlpatterns = [
    path('', root, name="index"),
    
    path('login', controllers.auth_con.view_login, name="login"),
    path('api/login', controllers.auth_con.Action_Login.as_view(), name="login-backend"),
    path('logout', controllers.auth_con.Action_Logout.as_view(), name="logout"),

    path('manage', controllers.manage.index, name="manage"),
    path('api/add/station', controllers.manage.Action_CreateStation.as_view(), name="add-station"),
    path('api/add/college', controllers.manage.Action_CreateCollege.as_view(), name="add-college"),

    path('college/<int:college_id>/sections', controllers.sections.SectionsView.as_view(), name="view-sections"),
    path('api/add/regular-section', controllers.sections.Action_CreateRegularSection.as_view(), name="add-regular-section"),
    path('api/add/merged-section', controllers.sections.Action_CreateMergedSection.as_view(), name="add-merged-section"),

    path('college/<int:college_id>/staff', controllers.staff.StaffView.as_view(), name="view-staff"),
    path('staff/<int:staff_id>/add-role', controllers.staff.AddRoleView.as_view(), name="view-add-role"),
    path('api/add/staff', controllers.staff.Action_CreateStaff.as_view(), name="add-staff"),
    path('api/add/staff-role', controllers.staff.Action_AddRole.as_view(), name="add-staff-role"),

    path('college/<int:college_id>/today/atnd', controllers.atnd_con.AttendanceView.as_view(), name='today-atnd'),
    path('api/atnd/update-atnd', controllers.atnd_con.Action_UpdateAtnd.as_view(), name="update-atnd"),

    path('college/<int:college_id>/time-table', controllers.timetable_con.TimeTableMainView.as_view(), name='view-timetable'),
    path(
        'table/<int:table_id>/add/section', 
        controllers.timetable_con.TimeTableAddSectionView.as_view(), 
        name='view-add-section-table'
    ),
    path('api/add/time-table', controllers.timetable_con.Action_CreateTimeTable.as_view(), name='add-table'),
    path('api/delete/time-table', controllers.timetable_con.Action_DeleteTimeTable.as_view(), name='delete-table'),
    path('api/table/add-section', controllers.timetable_con.Action_AddTimeTableSection.as_view(), name='table-add-section'),


    path(
        'college/<int:college_id>/today/lectures',
        controllers.lecture_con.LectureMainView.as_view(),
        name='view-lecture-today'
    ),
    path(
        'college/<int:college_id>/today/apply-fixture/<int:cell_id>',
        controllers.lecture_con.ApplyFixtureView.as_view(),
        name='view-apply-fix'
    ),
    path('api/mark-lec', controllers.lecture_con.Action_MarkComplete.as_view(), name='mark-lec'),
    path('api/apply-fix', controllers.lecture_con.Action_ApplyFixture.as_view(), name='apply-fix'),
    
    path('college/<int:college_id>/holidays', controllers.holidays_con.HolidaysView.as_view(), name='view-holidays'),
    path('api/add/holidays', controllers.holidays_con.Action_AddHoliday.as_view(), name='add-holidays'),


    path('rps/index', controllers.reports.MainAdminReportsView.as_view(), name='view-reports-main'),
    path('rps/atndsheet', controllers.reports.AtndSheetView.as_view(), name='view-rp-atnd'),
    path('rps/lecturesheet', controllers.reports.LectureSheetView.as_view(), name='view-rp-lecsheet'),


    path('roleps/<int:role_param_id>/create-acc', controllers.auth_con.UserAccountsView.as_view(), name="view-create-acc"),
    path('api/add/user', controllers.auth_con.Action_CreateUser.as_view(), name="add-user"),
    

    path('transfers/index', controllers.transfers.MainTransfersView.as_view(), name="view-transfers"),
    
    
    path('college/<int:college_id>/staff2', controllers.staff_v2.StaffView.as_view(), name="view-staff2"),
    path('staff/<int:staff_id>/add-role2', controllers.staff_v2.AddRoleView.as_view(), name="view-add-role2"),
    path('api/add/staff2', controllers.staff_v2.Action_CreateStaff.as_view(), name="add-staff2"),
    path('api/add/staff-role2', controllers.staff_v2.Action_AddRole.as_view(), name="add-staff-role2"),


    path('college/<int:college_id>/time-table2', controllers.timetable_new.TimeTableMainView.as_view(), name='view-timetable2'),



]
