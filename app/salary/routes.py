from django.urls import path, include
from app.salary.home import root

app_name = "sl_u"
urlpatterns = [
    path('', root),

    path('manage/', include('app.salary.core.admin.routes')),
    path('auth/', include('app.salary.core.auth.routes'))
]
