from django.db import models
from django.db.models import constraints, fields
from django.db.models.base import Model
from django.db.models.fields.related import ForeignKey
from sorl.thumbnail import ImageField
from django.contrib.auth import get_user_model

User = get_user_model()

class Recipe(models.Model):
    ingredients = models.ForeignKey(
        'Ingredients',
        on_delete=models.CASCADE,
        verbose_name='Ingredients for recipe',
    )

    tags = models.ForeignKey(
        'Tag',
        on_delete=models.SET_NULL,
        verbose_name='Tags',
        null=True
    )

    image = ImageField(
        upload_to='recipes/',
        blank=True,
        null=True,
        verbose_name='Image',
    )


    name = models.TextField(
        verbose_name='Recipe title',
        max_length=128,
    )

    text = models.TextField(
        verbose_name='Recipe text',
    )

    cooking_time = models.TimeField(
        verbose_name='Time to cook'
    )

    def __str__(self) -> str:
        return self.title

class Ingredients(models.Model):

    name = models.TextField(
        verbose_name='Ingredients title',
        max_length=128,
    )

    measurement_unit = models.CharField(
        max_length=10,
    )

    def __str__(self) -> str:
        return self.title

class Tag(models.Model):
    title = models.CharField(
        verbose_name='Tag title',
        max_length=50,
        unique=True,
    )

    slug = models.SlugField(
        verbose_name='Tag slug',
        unique=True
    )

    color = models.CharField(
        verbose_name='HEX formated color for tag',
        max_length=7
    )

    def __str__(self) -> str:
        return self.title
