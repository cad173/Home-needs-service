from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),   # 👈 ADD THIS
    path('login/', views.login_view, name='login'),
    path('dashboard/', views.dashboard, name='dashboard'),
]