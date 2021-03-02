from django.urls import path
from . import views

urlpatterns = [
    path('clg/<int:college_id>/index/', views.StaffView.as_view(), name='Staff.Index'),
    path('add/staff/fresh/', views.Action_CreateStaff.as_view(), name='Staff.Add'),
]
