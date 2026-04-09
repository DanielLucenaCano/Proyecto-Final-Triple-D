from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    company_name = models.CharField(max_length=255, blank=True)
    phone_number = models.CharField(max_length=50, blank=True)

    def __str__(self) -> str:
        return self.username
