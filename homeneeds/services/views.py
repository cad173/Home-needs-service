from django.shortcuts import render, redirect

def home(request):
    return render(request, 'services/home.html')

def login_view(request):
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')

        if email and password:
            return redirect('dashboard')

    return render(request, 'services/login.html')

def register_view(request):
    if request.method == "POST":
        first_name = request.POST.get('first_name')
        email = request.POST.get('email')
        password = request.POST.get('password')

        if first_name and email and password:
            return redirect('login')

    return render(request, 'services/register.html')

def dashboard(request):
    return render(request, 'services/dashboard.html')
