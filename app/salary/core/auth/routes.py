from django.urls import path
from . import views as auth_views

urlpatterns = [
    path('login/', auth_views.LoginView.as_view(), name='Auth.Login'),
    path('logout/', auth_views.logout_view, name='Auth.Logout'),
]
