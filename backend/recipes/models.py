from django.contrib.auth import get_user_model
from django.core import validators
from django.db import models

from colorfield.fields import ColorField

User = get_user_model()


class Ingredient(models.Model):
    name = models.CharField(
        max_length=128,
        verbose_name='Название ингредиента'
    )
    measurement_unit = models.CharField(
        max_length=128,
        verbose_name='Единицы измерений'
    )

    class Meta:
        ordering = ['-id']
        verbose_name ='Ингредиент'
        verbose_name_plural ='Ингредиенты'

    def __str__(self):
        return self.name


class Recipe(models.Model):
    author = models.ForeignKey(
        User,
        related_name='recipes',
        on_delete=models.CASCADE,
        verbose_name='Автор рецепта'
    )
    name = models.CharField(
        max_length=128,
        verbose_name='Название рецепта'
    )
    image = models.ImageField(
        upload_to='recipes/',
        verbose_name='Изображение рецепта'
    )
    ingredients = models.ManyToManyField(
        Ingredient,
        through='IngredientsInRecipe',
        verbose_name='Ингредиенты рецепта'
    )
    text = models.TextField(
        default='Text',
        verbose_name='Текст рецепта')
    tags = models.ManyToManyField(
        'Tag',
        verbose_name='Теги в рецепте')
    cooking_time = models.IntegerField(
        validators=(
            validators.MinValueValidator(
                1,
                message='Min 1 minute'
            ),
        ),
        verbose_name='Время готовки'
    )

    class Meta:
        ordering = ['-id']
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'

    def __str__(self):
        return self.name


class Tag(models.Model):
    name = models.CharField(
        max_length=128,
        unique=True,
        verbose_name='Название тега')
    color = ColorField('HEX цвет', default='#000000')
    slug = models.SlugField(
        max_length=128,
        unique=True,
        verbose_name='Слаг тега')

    class Meta:
        ordering = ['-id']
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'

    def __str__(self):
        return self.name


class IngredientsInRecipe(models.Model):
    ingredient = models.ForeignKey(
        'Ingredient',
        on_delete=models.CASCADE,
        related_name='ingredients_in_recipe',
        verbose_name='Ингредиент'
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='ingredients_in_recipe',
        verbose_name='Рецепт'
    )
    amount = models.IntegerField(
        validators=(
            validators.MinValueValidator(
                1,
                message='Min 1 ingredient'
            ),
        ),
        verbose_name='Количество ингредиентов'
    )

    class Meta:
        ordering = ['-id']
        verbose_name = 'Ингредиент в рецепте'
        verbose_name_plural = 'Ингредиенты в рецепте'
        constraints = [
            models.UniqueConstraint(
                fields=['recipe', 'ingredient'],
                name='uniq_ingredients_in_recipe'
            )
        ]

    def __str__(self) -> str:
        return str(self.ingredient)
