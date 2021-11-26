from django.contrib.auth import get_user_model
from django.db import models
from django.db.models import constraints, fields
from django.db.models.base import Model
from django.db.models.fields.related import ForeignKey
from sorl.thumbnail import ImageField

User = get_user_model()

class Recipe(models.Model):
    tags = models.ForeignKey(
        'Tag',
        on_delete=models.CASCADE,
        verbose_name='Tags',
    )

    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='author',
        verbose_name='author',
        null=True
    )

    ingredients = models.ManyToManyField(
        'Ingredients',
        verbose_name='Ingredients for recipe',
    )

    is_favorited = models.BooleanField(
        default=True
    )

    is_in_shopping_cart = models.BooleanField(
        default=False
    )

    name = models.TextField(
        verbose_name='Recipe title',
        max_length=128,
    )

    image = ImageField(
        upload_to='recipes/',
        blank=True,
        null=True,
        verbose_name='Image',
    )

    text = models.TextField(
        verbose_name='Recipe text',
    )

    cooking_time = models.IntegerField(
        verbose_name='Time to cook'
    )

    def __str__(self) -> str:
        return self.name

class Ingredients(models.Model):

    name = models.TextField(
        verbose_name='Ingredients title',
        max_length=128,
    )

    measurement_unit = models.CharField(
        max_length=10,
        null=True,
    )

    def __str__(self) -> str:
        return self.name

class Tag(models.Model):
    name = models.CharField(
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
        return self.name
