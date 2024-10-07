from django.shortcuts import render, redirect, get_object_or_404
from django.views import generic
from django.urls import reverse, reverse_lazy
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from functools import wraps

from .models import Task
from .forms import TaskForm

# Create your views here.
def index(request):
    return render(request, 'projectpage/index.html')

def login(request):
    return render(request, 'account/login.html')

def admin_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        admin_emails = ["iurivintonyak@gmail.com"]
        # print("Logged in user:", request.user)
        # print("Email:", request.user.email)
        if request.user.email in admin_emails:
            return view_func(request, *args, **kwargs)
        return HttpResponseForbidden("You do not have permission to access this page.")
    return _wrapped_view

@login_required
def dashboard(request):
    user_id = request.user
    full_name = request.user.get_full_name()
    context = {
        "full_name" : full_name,
        "user_id" : user_id,
    }
    return render(request, 'projectpage/dashboard.html', context)

@login_required
@admin_required
def admin_dashboard(request):
    user_id = request.user
    full_name = request.user.get_full_name()
    task_list = Task.objects.all()  # This retrieves all tasks

    context = {
        "full_name" : full_name,
        "user_id" : user_id,
        "task_list" : task_list,
    }
    return render(request, 'projectpage/admin_dashboard.html', context)

@login_required
@admin_required
def delete_task(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    task.delete()
    return redirect('projectpage:admin_dashboard')

def admin_login(request):
    return render(request, "account/admin_login.html")

# def add_task(request):
#     return render(request, 'projectpage/add_task.html')

class AddView(generic.CreateView):
    form_class = TaskForm
    template_name = "projectpage/add_task.html"

    success_url = reverse_lazy("projectpage:dashboard")

class TaskListView(generic.ListView):
    model = Task
    template_name = "projectpage/task_list.html"
    context_object_name = "task_list"