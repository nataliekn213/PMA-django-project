from django.shortcuts import render, redirect, get_object_or_404
from django.views import generic
from django.urls import reverse, reverse_lazy
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponseForbidden, FileResponse
from functools import wraps
from django.conf import settings
from django.core.files.storage import default_storage
from django.views.decorators.http import require_POST
from django.db.models import Q
import boto3

from .models import Task, Document, Project, Membership
from .forms import TaskForm, DocumentForm, ProjectForm
from django.http import JsonResponse



# Create your views here.
# def index(request):
#     return render(request, 'projectpage/index.html')

def index(request):
    projects = Project.objects.all()  # Fetch all projects from the database
    return render(request, 'projectpage/index.html', {'projects': projects})

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



def home(request):
    if not request.user.is_authenticated:
        # Only get limited project info for anonymous users
        projects = Project.objects.only('title', 'owner')
    else:
        # Fetch all projects with full details for logged-in users
        projects = Project.objects.all()
    
    return render(request, 'index.html', {'projects': projects})


@require_POST
def delete_project(request, project_id):
    # Get the project to delete
    project = get_object_or_404(Project, id=project_id)
    
    # Initialize S3 client
    s3 = boto3.client(
        's3',
        aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
        aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
        region_name=settings.AWS_S3_REGION_NAME
    )

    # Delete all files associated with the project from S3
    # Assuming tasks have a file field, and files are stored in a project-specific folder
    for document in project.documents.all():
        if document.file:  # Ensure there's a file to delete
            s3.delete_object(Bucket=settings.AWS_STORAGE_BUCKET_NAME, Key=document.file.name)
        document.delete()

    # Delete the project and related tasks
    project.delete()

    # Redirect back to the project list after deletion
    return redirect('projectpage:project_list')

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
                    file_title = document.title
                    file_description = document.description
                    file_keywords = document.keywords
                    # print(file_url);
                    print(document)
                except Exception as e:
                    print(e)
                return render(request, 'projectpage/upload.html', {
                    'file_url': file_url,
                    'file_extension': file_extension,
                    'file_title': file_title,
                    'file_description': file_description,
                    'file_keywords': file_keywords
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
def edit_task(request, pk):
    task = get_object_or_404(Task, pk=pk)
    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            project_id = request.POST.get('project')
            task.project = Project.objects.get(id=project_id)
            task.save()
            return redirect('projectpage:task_list')  # Redirect to task_list after saving
    return redirect('projectpage:task_list')

@login_required
def project_list(request):
    # projects = Project.objects.prefetch_related('members','tasks').all()  # Optimizes task loading
    cur_user = request.user
    projects = Project.objects.filter(
        Q(members=cur_user) | Q(owner=cur_user)
    ).distinct()
    context = {
        "projects":projects,
        "cur_user":cur_user,
    }
    return render(request, 'projectpage/project_list.html', context)




# class EditTaskView(generic.CreateView):
#     template_name = 'projectpage/edit_task.html'

#     def get(self, request, pk):
#         task = get_object_or_404(Task, pk=pk)
#         projects = Project.objects.all()
#         form = TaskForm(instance=task)
#         return render(request, self.template_name, {'form': form, 'task': task, 'projects': projects})

#     def post(self, request, pk):
#         task = get_object_or_404(Task, pk=pk)
#         form = TaskForm(request.POST, instance=task)
#         if form.is_valid():
#             project_id = request.POST.get('project')
#             project = Project.objects.get(id=project_id) if project_id else None
#             task.project = project
#             task.save()
#             return redirect('task_list')
#         projects = Project.objects.all()
#         return render(request, self.template_name, {'form': form, 'task': task, 'projects': projects})

class CreateProjectView(generic.CreateView):
    template_name = "projectpage/add_project.html"
    form_class = ProjectForm

    def get(self, request):
        print("getting")
        users = User.objects.all()
        form = ProjectForm()
        return render(request, self.template_name, {"form":form, "users":users})
    
    def post(self, request):
        form = self.form_class(request.POST)
        # print(f"form: {form}")
        if form.is_valid():
            # title = request.POST.get("title")
            # print(f"title: {title}")
            project = form.save(commit=False)
            project.owner = request.user
            project.save()
            form.save_m2m()
            return redirect("projectpage:dashboard")
        else:
            print(f"errors: {form.errors}")
            users = User.objects.all()
            return render(request, self.template_name, {"form":form, "users":users})
    
class AddView(generic.CreateView):
    template_name = 'projectpage/add_task.html'

    def get(self, request):
        projects = Project.objects.all()
        form = TaskForm()
        return render(request, self.template_name, {'form': form, 'projects': projects})

    def post(self, request):
        form = TaskForm(request.POST)
        if form.is_valid():
            project_id = request.POST.get('project')
            project = Project.objects.get(id=project_id) if project_id else None
            
            task = form.save(commit=False)
            task.project = project
            task.save()
            return redirect('projectpage:task_list')  # Ensure 'task_list' matches the name in urls.py
        else:
            projects = Project.objects.all()
            return render(request, self.template_name, {'form': form, 'projects': projects})

# class AddView(generic.CreateView):
#     form_class = TaskForm
#     template_name = "projectpage/add_task.html"

#     project_list = Project.objects.all()
#     context_object_name = "project_list"

#     success_url = reverse_lazy("projectpage:dashboard")

# class TaskListView(generic.ListView):
#     model = Task
#     template_name = "projectpage/task_list.html"
#     context_object_name = "tasks"

class TaskListView(generic.ListView):
    model = Task
    template_name = 'projectpage/task_list.html'
    context_object_name = 'tasks'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['projects'] = Project.objects.all() 
        return context