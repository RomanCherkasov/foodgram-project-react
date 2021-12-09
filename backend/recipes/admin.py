from django.contrib import admin
from recipes.models import Ingredient, IngredientsInRecipe, Recipe, Tag
from users.models import Favorite


class AdminRecipe(admin.ModelAdmin):
    list_display = ('author', 'name', 'favorite_count')
    empty_value_display = '--empty--'

    def favorite_count(self, instance):
        return Favorite.objects.filter(recipe=instance).count()


class AdminTag(admin.ModelAdmin):
    list_display = ('id', 'name', 'color', 'slug')
    empty_value_display = '--empty--'


class AdminIngredient(admin.ModelAdmin):
    list_display = ('name', 'measurement_unit')
    empty_value_display = '--empty--'


class AdminIngredientsInRecipe(admin.ModelAdmin):
    list_display = ('id', 'recipe', 'ingredient', 'amount')
    empty_value_display = '--empty--'


class AdminIngredientsInRecipeMany(admin.TabularInline):
    model = IngredientsInRecipe
    min_num = 1
    extra = 1


admin.site.register(Recipe, AdminRecipe)
admin.site.register(Tag, AdminTag)
admin.site.register(Ingredient, AdminIngredient)
admin.site.register(IngredientsInRecipe, AdminIngredientsInRecipe)
