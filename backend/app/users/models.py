from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    USER = 'user'
    ADMIN = 'admin'

    CHOICES = (
        (USER, 'user'),
        (ADMIN, 'admin'),
    )

    first_name = models.CharField(
        verbose_name='first name',
        max_length=150,
        blank=False
    )
    
    last_name = models.CharField(
        verbose_name='last name',
        max_length=150,
        blank=False
    )
    
    email = models.EmailField(
        verbose_name='email address',
        blank=False,
        max_length=254,
    )

    role = models.CharField(
        verbose_name='User Role',
        max_length=16,
        null=False,
        default=USER,
        choices=CHOICES,
    )

    password = models.CharField(
        verbose_name='User password',
        max_length=150,
    )

    REQUIRED_FIELDS = [
        'first_name',
        'last_name',
        'email',    
    ]

    def __str__(self) -> str:
        return self.email
