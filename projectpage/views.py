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
from django.db.models.functions import Lower
import boto3

from .models import Task, Document, Project, Membership, CustomUserProfile  # Updated import
from .forms import TaskForm, DocumentForm, ProjectForm
from django.http import JsonResponse
from django.db.models import Min

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
        try:
            # Check if the user has a CustomUserProfile and is a PMA admin
            profile = CustomUserProfile.objects.get(user=request.user)
            if profile.is_pma_admin:
                return view_func(request, *args, **kwargs)
        except CustomUserProfile.DoesNotExist:
            pass
        
        return render(request, 'projectpage/admin_permission_denied.html', status=403)
    return _wrapped_view

@login_required
def dashboard(request):
    user_id = request.user
    full_name = request.user.get_full_name()
    context = {
        "full_name": full_name,
        "user_id": user_id,
    }
    return render(request, 'projectpage/dashboard.html', context)



def home(request):
    if not request.user.is_authenticated:
        # Only get limited project info for anonymous users
        projects = Project.objects.only('title', 'description', 'owner')
    else:
        # Fetch all projects with full details for logged-in users
        projects = Project.objects.all()
    
    return render(request, 'index.html', {'projects': projects})


@require_POST
def delete_project(request, project_id):
    # Get the project to delete
    project = get_object_or_404(Project, id=project_id)

    if not request.user == project.owner:
        return HttpResponseForbidden("You do not have permission to delete this project.")

    # Initialize S3 client
    s3 = boto3.client(
        's3',
        aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
        aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
        region_name=settings.AWS_S3_REGION_NAME
    )

    # Delete all files associated with the project from S3
    for document in project.documents.all():
        if document.file:  # Ensure there's a file to delete
            s3.delete_object(Bucket=settings.AWS_STORAGE_BUCKET_NAME, Key=document.file.name)
        document.delete()

    # Delete the project and related tasks
    project.delete()

    # Redirect back to the project list after deletion
    return redirect('projectpage:admin_dashboard')

@login_required
@admin_required
def admin_dashboard(request):
    user_id = request.user
    full_name = request.user.get_full_name()

    # Retrieve all projects and files since PMA admins need to see everything
    projects = Project.objects.all()
    documents = Document.objects.all()

    context = {
        "full_name": full_name,
        "user_id": user_id,
        "projects": projects,
        "documents": documents,
    }
    return render(request, 'projectpage/admin_dashboard.html', context)

@login_required
@admin_required
def delete_task(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    task.delete()
    return redirect('projectpage:task_list')

@login_required
@require_POST
def delete_file(request, document_id):
    # Get the file object from the database
    document = get_object_or_404(Document, id=document_id)

    # Initialize the S3 client
    s3 = boto3.client(
        's3',
        aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
        aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
        region_name=settings.AWS_S3_REGION_NAME
    )

    # Delete the file from S3
    if document.file:
        try:
            s3.delete_object(Bucket=settings.AWS_STORAGE_BUCKET_NAME, Key=document.file.name)
        except Exception as e:
            # Handle any errors during the deletion
            print(f"Error deleting file from S3: {e}")
    
    # Delete the file record from the database
    document.delete()

    # Redirect back to the admin dashboard
    return redirect('projectpage:admin_dashboard')


def admin_login(request):
    return render(request, "registration/admin_login.html")

@login_required
def upload(request):
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES, user=request.user)
        if form.is_valid():
            file = form.cleaned_data['file']
            file_name = file.name
            file_extension = file_name.split('.')[-1].lower()  # Get the file extension

            file_url = file_title = file_description = file_keywords = None  # Initialize variables

            if settings.USE_S3:
                try:
                    document = Document(
                        file=file,
                        title=form.cleaned_data['title'],
                        description=form.cleaned_data['description'],
                        keywords=form.cleaned_data['keywords'],
                        project=form.cleaned_data['project']
                    )
                    document.save()
                    file_url = document.file.url
                    file_title = document.title
                    file_description = document.description
                    file_keywords = document.keywords
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
        form = DocumentForm(user=request.user)
        projects = form.fields['project'].queryset

    return render(request, 'projectpage/upload.html', {'form': form,
                                                       'projects': projects})

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
            return redirect('projectpage:task_list')
    return redirect('projectpage:task_list')

@login_required
def project_list(request):
    # cur_user = request.user
    # sort_by = request.GET.get("sort", "alphabetical")
    
    # if sort_by == "date":
    #     projects = Project.objects.filter(
    #         Q(members=cur_user) | Q(owner=cur_user)
    #     ).annotate(
    #         earliest_task_date=Min("tasks__deadline")
    #     ).order_by("earliest_task_date", "title").distinct()
    # elif sort_by == "alphabetical":
    #     projects = Project.objects.filter(
    #         Q(members=cur_user) | Q(owner=cur_user)
    #     ).order_by("title").distinct()
    # else:
    #     projects = Project.objects.filter(
    #         Q(members=cur_user) | Q(owner=cur_user)
    #     ).order_by("title").distinct()

    # context = {
    #     "projects": projects,
    #     "cur_user": cur_user,
    # }
    # return render(request, "projectpage/project_list.html", context)
    sort_option = request.GET.get('sort', 'date')
    if sort_option == 'date':
        projects_with_tasks = Project.objects.annotate(
            earliest_task_due=Min('tasks__deadline')
        ).filter(earliest_task_due__isnull=False).order_by('earliest_task_due', 'title')

        projects_without_tasks = Project.objects.annotate(
            earliest_task_due=Min('tasks__deadline')
        ).filter(earliest_task_due__isnull=True).order_by('title')

        projects = list(projects_with_tasks) + list(projects_without_tasks)

    elif sort_option == 'alphabetical':
        projects = Project.objects.all().order_by(Lower('title'))

    else:
        projects = Project.objects.all()    

    documents = Document.objects.filter(project__in=projects)
    context = {
        "projects": projects,
        "documents": documents,
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
        users = User.objects.all()
        form = ProjectForm()
        return render(request, self.template_name, {"form": form, "users": users})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            project = form.save(commit=False)
            project.owner = request.user
            project.save()
            form.save_m2m()
            return redirect("projectpage:dashboard")
        else:
            users = User.objects.all()
            return render(request, self.template_name, {"form": form, "users": users})

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
            return redirect('projectpage:task_list')
        else:
            projects = Project.objects.all()
            return render(request, self.template_name, {'form': form, 'projects': projects})

class TaskListView(generic.ListView):
    model = Task
    template_name = 'projectpage/task_list.html'
    context_object_name = 'tasks'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['projects'] = Project.objects.all()
        return context
