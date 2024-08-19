from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    address = models.CharField(max_length=255, blank=True)
    phone_number = models.CharField(max_length=15, blank=True)
    saved_payment_method = models.CharField(max_length=255, blank=True)  # Placeholder 

    def __str__(self):
        return self.user.username