from django.urls import path, include

from . import views

app_name = "projectpage"
urlpatterns = [
    path("", views.index, name="index"),
    path("dashboard/", views.dashboard, name="dashboard"),
    path("account/login", views.login, name="login"),
    path("account/admin_login", views.admin_login, name="admin_login"),
    path("admin_dashboard/", views.admin_dashboard, name="admin_dashboard"),
    path("dashboard/add_task", views.AddView.as_view(), name="add_task"),
]