from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()

class IsSubscribed(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='subscriber',)

    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='subscribing',)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['user','author'],
                name='unique_subs'
            )
        ]
