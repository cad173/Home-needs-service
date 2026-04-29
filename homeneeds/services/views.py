from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout


def home(request):
    return render(request, 'services/home.html')


def login_view(request):
    error = None

    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')

        user = authenticate(request, username=email, password=password)

        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            error = "Invalid email or password"

    return render(request, 'services/login.html', {'error': error})


def register_view(request):
    if request.method == "POST":
        first_name = request.POST.get('first_name')
        email = request.POST.get('email')
        password = request.POST.get('password')

        if first_name and email and password:
            User.objects.create_user(
                username=email,
                email=email,
                password=password
            )
            return redirect('login')

    return render(request, 'services/register.html')


@login_required
def dashboard(request):
    return render(request, 'services/dashboard.html')


def logout_view(request):
    logout(request)
    return redirect('home')