from django.shortcuts import render

# Create your views here.
def index(request):
    return render(request, 'projectpage/index.html')

def login(request):
    return render(request, 'account/login.html')

def dashboard(request):
    return render(request, 'projectpage/dashboard.html')