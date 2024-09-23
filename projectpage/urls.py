from django.urls import path

from . import views

app_name = "projectpage"
urlpatterns = [
    path("", views.index, name="index"),
]