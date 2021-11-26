from django.contrib.auth.models import AbstractUser
from django.db import models


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
        unique=True
    )

    role = models.CharField(
        verbose_name='User Role',
        max_length=16,
        null=False,
        default=USER,
        choices=CHOICES,
    )
    is_subscribed = models.BooleanField(
        default=False
    )

    password = models.CharField(
        verbose_name='User password',
        max_length=150,
    )
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = [
        'username',
        'first_name',
        'last_name', 
    ]

    def __str__(self) -> str:
        return self.email



class IsSubscribed(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='subscriber',
    )

    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='subscribing', 
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['user','author'],
                name='unique_subs'
            )
        ]
