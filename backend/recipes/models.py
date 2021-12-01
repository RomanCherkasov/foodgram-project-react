from re import S
from django.core import validators
from django.db import models
from django.contrib.auth import get_user_model
from django.db.models import constraints, fields

User = get_user_model()

class Recipe(models.Model):
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )
    name = models.CharField(
        max_length=128
    )
    image = models.ImageField(
        upload_to='recipes/'
    )
    ingredients = models.ManyToManyField(
        'Ingredient',
        through='IngredientsInRecipe',
    )
    tags = models.ManyToManyField('Tag')
    cooking_time = models.IntegerField(
        validators=(
            validators.MinValueValidator(
                1,
                message='Min 1 minute'
            ),
        ),
    )

    def __str__(self):
        return self.name
    
class Ingredient(models.Model):
    name = models.CharField(
        max_length=128
    )
    measurement_unit = models.CharField(
        max_length=128
    )

    def __str__(self):
        return self.name

class Tag(models.Model):
    from colorfield.fields import ColorField
    name = models.CharField(
        max_length=128,
        unique=True)
    color = ColorField('HEX Color', default='#000000')
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name

class IngredientsInRecipe(models.Model):
    ingredient = models.ForeignKey(
        'Ingredient',
        on_delete=models.CASCADE
    )
    recipe = models.ForeignKey(
        'Recipe',
        on_delete=models.CASCADE
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
        return f'{str(self.ingredient)}:{str(self.recipe)}'
