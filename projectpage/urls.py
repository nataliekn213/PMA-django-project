from django.urls import path, include

from . import views

app_name = "projectpage"
urlpatterns = [
    path("", views.index, name="index"),
    path("dashboard/", views.dashboard, name="dashboard"), 
    # path('accounts/', include('allauth.urls')),
]

app_name = "account"
urlpatterns = [
    path("login/", views.login, name="login"),
]