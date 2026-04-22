from django.shortcuts import render, redirect

def login_view(request):
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')

        # simple check (for now)
        if email and password:
            return redirect('dashboard')

    return render(request, 'services/login.html')

def dashboard(request):
    return render(request, 'services/dashboard.html')

def home(request):
    return render(request, 'services/home.html')