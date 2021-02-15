from django.urls import path
from . import views as admin_views

urlpatterns = [
    path('index/', admin_views.IndexManageView.as_view(), name='Manage.Index'),
    path('add/station/', admin_views.Action_CreateStation.as_view(), name='Manage.AddStation'),
    path('add/college/', admin_views.Action_CreateCollege.as_view(), name='Manage.AddCollege')
]
