from django.urls import path
from . import views

urlpatterns = [
    path('college/<int:college_id>/index', views.SectionsView.as_view(), name="Section.Index"),
    path('add/regular', views.Action_CreateRegularSection.as_view(), name="Section.AddReg"),
]
