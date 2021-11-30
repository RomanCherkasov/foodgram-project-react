from django.contrib.auth import get_user_model
from django.core import validators
from django.db import models
from colorfield.fields import ColorField
from django.db.models.base import Model

User = get_user_model()

class Ingredients(models.Model):

    name = models.TextField(
        verbose_name='Ingredients title',
        max_length=128,)

    measurement_unit = models.CharField(
        max_length=10,
        null=True,)

    def __str__(self) -> str:
        return self.name

class Recipe(models.Model):
    tags = models.ManyToManyField(
        'Tag',
        verbose_name='Tags',)

    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='recipe',
        verbose_name='author',)

    ingredients = models.ManyToManyField(
        Ingredients,
        through='IngredientsInRecipe',
        verbose_name='Ingredients for recipe',)

    # is_favorited = models.BooleanField(
    #     default=True)

    # is_in_shopping_cart = models.BooleanField(
    #     default=False)

    name = models.TextField(
        verbose_name='Recipe title',
        max_length=128,)

    image = models.ImageField(
        upload_to='recipes/',
        verbose_name='Image',)

    text = models.TextField(
        verbose_name='Recipe text',)

    cooking_time = models.IntegerField(
        verbose_name='Time to cook',
        validators=(
            validators.MinValueValidator(1)
        )
    )

    def __str__(self) -> str:
        return self.name

class IngredientsInRecipe(models.Model):
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='ingredients_in_recipe'
    )
    ingredient = models.ForeignKey(
        Ingredients,
        on_delete=models.CASCADE,
        related_name='ingredients_in_recipe'
    )
    amount = models.IntegerField(
        verbose_name='Time to cook',
        validators=(
            validators.MinValueValidator(1)
        )
    )
    constraints=[
        models.UniqueConstraint(
            fields=['recipe','ingredient']
        )
    ]

class Tag(models.Model):
    name = models.CharField(
        verbose_name='Tag title',
        max_length=50,
        unique=True,)

    slug = models.SlugField(
        verbose_name='Tag slug',
        unique=True)
    # ??? Django Colorfield https://pypi.org/project/django-colorfield/ ???
    # https://stackoverflow.com/questions/39859224/how-to-use-html5-color-picker-in-django-admin
    color = ColorField(
        # verbose_name='HEX formated color for tag',
        default='#FF0000')

    def __str__(self) -> str:
        return self.name
