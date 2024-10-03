from django.urls import path, include

from . import views

app_name = "projectpage"
urlpatterns = [
    path("", views.index, name="index"),
    path("login/", views.login, name="login"),
    path("dashboard/", views.dashboard, name="dashboard"), 
    path('accounts/', include('allauth.urls')),
]