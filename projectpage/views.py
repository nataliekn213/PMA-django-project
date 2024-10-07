from django.shortcuts import render, redirect
from django.views import generic
from django.urls import reverse, reverse_lazy

from .models import Task
from .forms import TaskForm

# Create your views here.
def index(request):
    return render(request, 'projectpage/index.html')

def login(request):
    return render(request, 'account/login.html')

def dashboard(request):
    user_id = request.user
    full_name = request.user.get_full_name()
    context = {
        "full_name" : full_name,
        "user_id" : user_id,
    }
    return render(request, 'projectpage/dashboard.html', context)

def admin_dashboard(request):
    user_id = request.user
    full_name = request.user.get_full_name()
    context = {
        "full_name" : full_name,
        "user_id" : user_id,
    }
    return render(request, 'projectpage/admin_dashboard.html', context)

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