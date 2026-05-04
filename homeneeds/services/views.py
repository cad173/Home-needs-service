from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.db.models import Q
from .models import Service, ProviderProfile, Profile

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


@login_required
def service_search(request):
    service_type = request.GET.get('service_type', '').strip()
    location = request.GET.get('location', '').strip()
    availability = request.GET.get('availability', '').strip()

    services = Service.objects.all()
    providers = ProviderProfile.objects.select_related('user').all()

    if service_type:
        services = services.filter(
            Q(category__icontains=service_type) | Q(service_name__icontains=service_type)
        )

    if location:
        providers = providers.filter(
            Q(user__city__icontains=location)
            | Q(user__state__icontains=location)
            | Q(user__zip_code__icontains=location)
        )

    if availability:
        providers = providers.filter(availability_status__icontains=availability)

    categories = Service.objects.values_list('category', flat=True).distinct().order_by('category')

    context = {
        'services': services,
        'providers': providers,
        'categories': categories,
        'service_type': service_type,
        'location': location,
        'availability': availability,
        'result_count': services.count() + providers.count(),
        'searched': any([service_type, location, availability]),
    }
    return render(request, 'services/service_search.html', context)