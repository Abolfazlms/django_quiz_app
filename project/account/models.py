# account/models.py
from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    phone_number = models.CharField(max_length=15, unique=True, verbose_name='phone number', blank=True, null=True)

    def __str__(self):
        return self.username
