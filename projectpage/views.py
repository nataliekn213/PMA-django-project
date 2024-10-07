from django.shortcuts import render

# Create your views here.
def index(request):
    return render(request, 'projectpage/index.html')

def login(request):
    return render(request, 'account/login.html')

def dashboard(request):
    return render(request, 'projectpage/dashboard.html')

def admin_dashboard(request):
    return render(request, 'projectpage/admin_dashboard.html')

def admin_login(request):
    return render(request, "account/admin_login.html")

def add_task(request):
    return render(request, 'projectpage/add_task.html')