from django.urls import path, include
from app.salary.home import root
from app.salary.core.exceptions import HttpNotFound

from django.shortcuts import render

app_name = "sl_u"
urlpatterns = [
    path('', root),

    # fmt: off
    path('manage/',     include('app.salary.core.admin.routes')),
    path('auth/',       include('app.salary.core.auth.routes')),
    path('sectioning/', include('app.salary.core.section.routes')),
    # fmt: on
]
