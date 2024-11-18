from django import forms
from django.contrib import admin
from django.contrib.auth.models import User
from .models import Task, Document, Project, Membership
from .forms import ProjectForm

# Register your models here.
admin.site.register(Task)
admin.site.register(Document)
admin.site.register(Membership)

class ProjectAdmin(admin.ModelAdmin):
    form = ProjectForm
    list_display = ("title", "owner", "get_members", "get_tasks")

    def get_members(self, obj):
        return ", ".join([member.username for member in obj.members.all()])
    get_members.short_description = "Members"

    def get_tasks(self, obj):
        return ", ".join([task.title for task in obj.tasks.all()])
    get_tasks.short_description = "Tasks"

admin.site.register(Project, ProjectAdmin)