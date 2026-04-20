from django.contrib import admin

from django.contrib import admin
from .models import User, ProviderProfile, ClientProfile, Service, JobRequest, Booking, Payment, Review

admin.site.register(User)
admin.site.register(ProviderProfile)
admin.site.register(ClientProfile)
admin.site.register(Service)
admin.site.register(JobRequest)
admin.site.register(Booking)
admin.site.register(Payment)
admin.site.register(Review)
