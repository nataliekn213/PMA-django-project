from django.urls import path, include

from . import views

app_name = "projectpage"
urlpatterns = [
    path("", views.index, name="index"),
    path('accounts/', include('allauth.urls')),
]