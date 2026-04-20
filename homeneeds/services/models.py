from django.db import models

from django.db import models


class User(models.Model):
    USER_TYPE_CHOICES = [
        ('provider', 'Provider'),
        ('client', 'Client'),
    ]

    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20)
    password = models.CharField(max_length=128)
    address = models.CharField(max_length=100)
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    zip_code = models.CharField(max_length=10)
    user_type = models.CharField(max_length=20, choices=USER_TYPE_CHOICES)
    background_check_status = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class ProviderProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    travel_radius = models.IntegerField()
    hourly_rate = models.DecimalField(max_digits=8, decimal_places=2)
    experience_years = models.IntegerField()
    availability_status = models.CharField(max_length=50)

    def __str__(self):
        return f"Provider: {self.user.first_name} {self.user.last_name}"


class ClientProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    preferred_contact_method = models.CharField(max_length=50)

    def __str__(self):
        return f"Client: {self.user.first_name} {self.user.last_name}"


class Service(models.Model):
    service_name = models.CharField(max_length=100)
    description = models.TextField()
    category = models.CharField(max_length=100)

    def __str__(self):
        return self.service_name


class JobRequest(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('completed', 'Completed'),
    ]

    client = models.ForeignKey(ClientProfile, on_delete=models.CASCADE)
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    job_description = models.TextField()
    job_location = models.CharField(max_length=100)
    requested_date = models.DateField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')

    def __str__(self):
        return f"Job {self.id} - {self.service.service_name}"


class Booking(models.Model):
    STATUS_CHOICES = [
        ('scheduled', 'Scheduled'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]

    job = models.ForeignKey(JobRequest, on_delete=models.CASCADE)
    provider = models.ForeignKey(ProviderProfile, on_delete=models.CASCADE)
    booking_date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)

    def __str__(self):
        return f"Booking {self.id}"


class Payment(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('paid', 'Paid'),
        ('failed', 'Failed'),
    ]

    booking = models.ForeignKey(Booking, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_date = models.DateField()
    payment_status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    payment_method = models.CharField(max_length=50)

    def __str__(self):
        return f"Payment {self.id}"


class Review(models.Model):
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE)
    rating = models.IntegerField()
    comment = models.TextField()
    review_date = models.DateField()

    def __str__(self):
        return f"Review {self.id}"
