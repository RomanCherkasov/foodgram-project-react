from django.contrib.auth import get_user_model
from django.core import validators
from django.db import models

from colorfield.fields import ColorField

User = get_user_model()


class Ingredient(models.Model):
    name = models.CharField(
        max_length=128
    )
    measurement_unit = models.CharField(
        max_length=128
    )

    def __str__(self):
        return self.name


class Recipe(models.Model):
    author = models.ForeignKey(
        User,
        related_name='recipes',
        on_delete=models.CASCADE
    )
    name = models.CharField(
        max_length=128
    )
    image = models.ImageField(
        upload_to='recipes/'
    )
    ingredients = models.ManyToManyField(
        Ingredient,
        through='IngredientsInRecipe',
    )
    text = models.TextField(default='Text')
    tags = models.ManyToManyField('Tag')
    cooking_time = models.IntegerField(
        validators=(
            validators.MinValueValidator(
                1,
                message='Min 1 minute'
            ),
        ),
    )

    class Meta:
        ordering = ['-id']

    def __str__(self):
        return self.name


class Tag(models.Model):
    name = models.CharField(
        max_length=128,
        unique=True)
    color = ColorField('HEX Color', default='#000000')
    slug = models.SlugField(max_length=128, unique=True)

    class Meta:
        ordering = ['-id']

    def __str__(self):
        return self.name


class IngredientsInRecipe(models.Model):
    ingredient = models.ForeignKey(
        'Ingredient',
        on_delete=models.CASCADE,
        related_name='ingredients_in_recipe',
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='ingredients_in_recipe',
    )
    amount = models.IntegerField(
        validators=(
            validators.MinValueValidator(
                1,
                message='Min 1 ingredient'
            ),
        ),
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['recipe', 'ingredient'],
                name='uniq_ingredients_in_recipe'
            )
        ]

    def __str__(self) -> str:
        return str(self.ingredient)
