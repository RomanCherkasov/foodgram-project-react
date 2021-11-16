from django.db import models
from django.db.models.fields.related import ForeignKey
from sorl.thumbnail import ImageField
from django.contrib.auth import get_user_model

User = get_user_model()

class Recipe(models.Model):
    title = models.TextField(
        verbose_name='Recipe title',
        max_length=128,
    )

    text = models.TextField(
        verbose_name='Recipe text',
    )

    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='recipes',
        verbose_name='Recipes author',
    )

    image = ImageField(
        upload_to='recipes/',
        blank=True,
        null=True,
        verbose_name='Image',
    )

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

    time = models.TimeField(
        verbose_name='Time to cook'
    )

class Ingredients(models.Model):
    KG = 'KG'
    GR = 'GR'
    UNITS = (
        (KG, 'KG'),
        (GR, 'GR'),
    )


    title = models.TextField(
        verbose_name='Ingredients title',
        max_length=128,
    )

    amount = models.IntegerField(
        verbose_name='Ingredients amount',
    )

    units = models.CharField(
        max_length=2,
        choices=UNITS,
        default=GR,
    )

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