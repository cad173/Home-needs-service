from django.shortcuts import render

def home(request):
    return render(request, 'services/home.html')

def login_view(request):
    return render(request, 'services/login.html')

def register_view(request):
    return render(request, 'services/register.html')

def dashboard(request):
    return render(request, 'services/dashboard.html')