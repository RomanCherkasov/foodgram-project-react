from django.contrib import admin

from users.models import Cart, Favorite


class AdminFavorite(admin.ModelAdmin):
    list_display = ('id', 'user', 'recipe')
    empty_value_display = "-пусто-"


class AdminCart(admin.ModelAdmin):
    list_display = ('id', 'user', 'recipe')
    empty_value_display = "-пусто-"


admin.site.register(Favorite, AdminFavorite)
admin.site.register(Cart, AdminCart)
