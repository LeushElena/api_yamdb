from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core import validators

class CustomUser(AbstractUser):
    bio = models.TextField(blank=True, null=True, max_length=200)
    role = models.CharField(max_length=20, default='user')
    email = models.EmailField(validators=[validators.validate_email],
        unique=True,
        blank=False)
    username = models.CharField(null=True, blank=True, max_length=150)
    confirmation_code = models.CharField(null=True, blank=True, max_length=255)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['confirmation_code', 'username']

    def __str__(self):
        return self.email