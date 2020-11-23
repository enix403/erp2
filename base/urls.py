"""base URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
# from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect
# from django.shortcuts import  render

import debug_toolbar

# def main_view(req):
    # return render(req, "sl/spaindex.html")
    

# urlpatterns = [
    # path("", main_view)
# ]


urlpatterns = [
    path("", lambda req: redirect("sl_u:index")),
    # path('admin/', admin.site.urls),
    path("sl/", include("salary.routes")),
    
    path('__debug__/', include(debug_toolbar.urls)),
]
