from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import PermissionsMixin
from django.core import validators
from datetime import datetime

class CustomUser(AbstractUser):
    username = models.CharField(blank=True, null=True, max_length=50)
    bio = models.TextField(blank=True, null=True, max_length=200)
    role = models.CharField(max_length=20, default='user')
    email = models.EmailField(validators=[validators.validate_email],
        unique=True,
        blank=False)
    confirmation_code = models.CharField(max_length=255, unique=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['confirmation_code']

    def __str__(self):
        return self.email

    @property
    def token(self):
        return self._generate_jwt_token()

    def _generate_jwt_token(self):
        dt = datetime.now() + timedelta(days=60)

        token = jwt.encode({
            'id': self.pk,
            'exp': int(dt.strftime('%s'))
        }, settings.SECRET_KEY, algorithm='HS256')

        return token.decode('utf-8')
