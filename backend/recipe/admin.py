from django.contrib import admin

from .models import (Ingredient, Recipe, Recipeingredients, RecipesFavorites,
                     RecipeTag, ShoppingCart, Tag)


class RecipeingredientsInline(admin.TabularInline):
    model = Recipeingredients
    extra = 1


class RecipeTagInline(admin.TabularInline):
    model = RecipeTag
    extra = 1


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    fields = (
        'author', 'name', 'image',
        'text', 'cooking_time',
        'get_ingredients'
    )
    list_display = ('name', 'author')
    list_filter = ('author', 'name', 'tags')
    inlines = [RecipeingredientsInline, RecipeTagInline]


@admin.register(Ingredient)
class IngredientsAdmin(admin.ModelAdmin):
    list_display = ('name', 'measurement_unit')
    list_filter = ('name',)


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    pass


@admin.register(RecipesFavorites)
class RecipesFavoritesAdmin(admin.ModelAdmin):
    pass


@admin.register(ShoppingCart)
class ShoppingCartAdmin(admin.ModelAdmin):
    pass
