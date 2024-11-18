from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from .models import Task, Document, Project, Membership, CustomUser
from .forms import ProjectForm

# Register your models
admin.site.register(Task)
admin.site.register(Document)
admin.site.register(Membership)

# Custom admin for Project
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

# Define an inline admin descriptor for CustomUser model
class CustomUserInline(admin.StackedInline):
    model = CustomUser
    can_delete = False
    verbose_name_plural = 'PMA Access'

# Customize the existing User admin to include the CustomUser fields
class UserAdmin(BaseUserAdmin):
    inlines = (CustomUserInline,)
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'get_is_pma')
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'customuser__is_pma')

    def get_is_pma(self, obj):
        return obj.customuser.is_pma if hasattr(obj, 'customuser') else False
    get_is_pma.boolean = True
    get_is_pma.short_description = 'PMA Admin'

# Re-register the User admin
admin.site.unregister(User)
admin.site.register(User, UserAdmin)
