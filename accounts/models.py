from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    #definisco i ruoli richiesti dalla traccia
    ROLE_CHOICES = (
        ('customer', 'Customer'),
        ('manager', 'Store Manager'),
    )
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='customer')

    def is_manager(self):
        return self.role == 'manager'