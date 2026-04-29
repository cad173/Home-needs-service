from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from .models import Profile  

# 🏠 Home Page
def home(request):
    return render(request, 'services/home.html')


# 🔐 Register View
def register_view(request):
    if request.method == "POST":
        first_name = request.POST.get('first_name')
        email = request.POST.get('email')
        password = request.POST.get('password')

        phone = request.POST.get('phone')
        address = request.POST.get('address')
        city = request.POST.get('city')
        state = request.POST.get('state')
        zipcode = request.POST.get('zipcode')
        user_type = request.POST.get('user_type')

        # ❗ Prevent duplicate users
        if User.objects.filter(username=email).exists():
            return render(request, 'services/register.html', {
                'error': 'User already exists'
            })

        if first_name and email and password:
            # Create Django user
            user = User.objects.create_user(
                username=email,
                email=email,
                password=password
            )

            # Save extra basic info
            user.first_name = first_name
            user.save()

            # Create Profile (your ER model)
            Profile.objects.create(
                user=user,
                phone=phone,
                address=address,
                city=city,
                state=state,
                zipcode=zipcode,
                user_type=user_type,
            )

            return redirect('login')

    return render(request, 'services/register.html')


# 🔐 Login View
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


# 📊 Dashboard (Protected)
@login_required
def dashboard(request):
    profile = Profile.objects.filter(user=request.user).first()

    return render(request, 'services/dashboard.html', {
        'user': request.user,
        'profile': profile
    })


# 🚪 Logout
def logout_view(request):
    logout(request)
    return redirect('home')