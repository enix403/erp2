from django.shortcuts import redirect
from django.urls import path, include

app_name = "sl_u"
urlpatterns = [
    path('', lambda r: redirect('sl_u:Manage.Index')),

    path('manage/', include('app.salary.core.admin.routes'))
]
