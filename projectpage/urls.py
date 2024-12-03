from django.urls import path, include
from django.contrib.auth import views as auth_views
from . import views

app_name = "projectpage"
urlpatterns = [
    path("", views.index, name="index"),
    path("dashboard/", views.dashboard, name="dashboard"),
    path("registration/login", views.login, name="login"),
    path("registration/admin_login", views.admin_login, name="admin_login"),
    path("admin_dashboard/", views.admin_dashboard, name="admin_dashboard"),
    path("dashboard/add_task", views.AddView.as_view(), name="add_task"),
    path("dashboard/add_project", views.CreateProjectView.as_view(), name="add_project"),
    path("dashboard/task_list", views.TaskListView.as_view(), name="task_list"),
    path('dashboard/upload/', views.upload, name="upload"),
    path("task/delete/<int:task_id>/", views.delete_task, name="delete_task"),
    path('task/<int:task_id>/complete/', views.complete_task, name='complete_task'),
    path('task_list/', views.TaskListView.as_view(), name='task_list'),
    path('task/<int:pk>/edit/', views.edit_task, name='edit_task'),

    # Project and File Deletion URLs
    path('project_list/', views.project_list, name='project_list'),
    path("all_projects/", views.all_projects, name="all_projects"),
    path('project/<int:project_id>/delete/', views.delete_project, name='delete_project'),
    path('file/<int:document_id>/delete/', views.delete_file, name='delete_file'),  # New URL for file deletion

    # Authentication URLs
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('login/', auth_views.LoginView.as_view(), name="login"),
    path('', views.home, name='home'),
    path('projectpage/', views.index, name='index'),


]
