from django.shortcuts import render, redirect, get_object_or_404
from django.views import generic
from django.urls import reverse, reverse_lazy
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden, FileResponse
from functools import wraps
from django.conf import settings
from django.core.files.storage import default_storage

from .models import Task, Document
from .forms import TaskForm, DocumentForm
from django.http import JsonResponse



# Create your views here.
def index(request):
    return render(request, 'projectpage/index.html')

def login(request):
    return render(request, 'registration/login.html')

def admin_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        admin_emails = ["iurivintonyak@gmail.com", "aadarsh.natarajan@gmail.com", "nataliekn213@gmail.com", "nouraalghamdi10@gmail.com", "ccook6387@gmail.com", "test_admin@test.com"]
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
    return redirect('projectpage:task_list')

def admin_login(request):
    return render(request, "registration/admin_login.html")

# def add_task(request):
#     return render(request, 'projectpage/add_task.html')

@login_required
def upload(request):
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            file = form.cleaned_data['file']
            file_name = file.name
            file_extension = file_name.split('.')[-1].lower()  # Get the file extension
            if settings.USE_S3:
                try:
                    document = Document(file=file, title=form.cleaned_data['title'], description=form.cleaned_data['description'], keywords=form.cleaned_data['keywords'])
                    document.save()
                    file_url = document.file.url
                    # print(file_url);
                    print(document)
                except Exception as e:
                    print(e)
            # else:
            #     fs = FileSystemStorage()
            #     filename = fs.save(file.name, file)
            #     file_url = fs.url(filename)
                return render(request, 'projectpage/upload.html', {
                    'file_url': file_url, 'file_extension': file_extension,
                })
    else:
        form = DocumentForm()
    return render(request, 'projectpage/upload.html')

@login_required
@admin_required
def complete_task(request, task_id):
    if request.method == "POST":
        task = get_object_or_404(Task, id=task_id)
        task.is_completed = not task.is_completed
        task.save()
        return JsonResponse({'success': True, 'is_completed': task.is_completed})

@login_required
def edit_task(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    if request.method == 'POST':
        task.title = request.POST.get('title', task.title)
        task.deadline = request.POST.get('deadline', task.deadline)
        task.save()
        return redirect('projectpage:task_list')




class AddView(generic.CreateView):
    form_class = TaskForm
    template_name = "projectpage/add_task.html"

    success_url = reverse_lazy("projectpage:dashboard")

class TaskListView(generic.ListView):
    model = Task
    template_name = "projectpage/task_list.html"
    context_object_name = "task_list"