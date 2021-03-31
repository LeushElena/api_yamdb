from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core import validators

class CustomUser(AbstractUser):
    ROLE_USER = 'user'
    ROLE_MODERATOR = 'moderator'
    ROLE_ADMIN = 'admin'
    USERS_ROLE = (
        (ROLE_USER, 'Пользователь'),
        (ROLE_MODERATOR, 'Модератор'),
        (ROLE_ADMIN, 'Админ'),
    )
    bio = models.TextField(blank=True, null=True, max_length=200)
    role =  models.CharField(
        verbose_name='Роль пользователя',
        max_length=10,
        choices=USERS_ROLE,
        default=ROLE_USER,
    )
    email = models.EmailField(validators=[validators.validate_email],
        unique=True,
        blank=False)
    username = models.CharField(null=True, blank=True, max_length=150, unique=True)
    confirmation_code = models.CharField(null=True, blank=True, max_length=255)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['confirmation_code', 'username']

    def __str__(self):
        return self.email

    
class Category(models.Model):
    name = models.CharField(unique=True, max_length=200)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name


class Genre(models.Model):
    name = models.CharField(unique=True, max_length=200)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name


class Title(models.Model):
    name = models.CharField(max_length=200)
    year = models.PositiveSmallIntegerField(blank=True, null=True)
    category = models.ForeignKey(Category, 
                                 on_delete=models.SET_NULL,
                                 blank=True, null=True)
    description = models.CharField(max_length=1000, blank=True)
    genre = models.ManyToManyField(Genre,
                                   related_name="genre_titles")
    
