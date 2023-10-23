from django_filters.rest_framework import (CharFilter, FilterSet,
                                           ModelChoiceFilter, filters)

from recipe.models import Ingredient, Recipe, Tag
from users.models import User


class FilterRecipe(FilterSet):
    tags = filters.ModelMultipleChoiceFilter(
        queryset=Tag.objects.all(),
        field_name='tags__slug',
        to_field_name='slug'
    )
    author = ModelChoiceFilter(
        queryset=User.objects.all()
    )
    is_favorited = filters.NumberFilter(
        method='get_is_favorited',
        field_name='is_favorited',
    )
    is_in_shopping_cart = filters.NumberFilter(
        method='get_is_in_shopping_cart',
        field_name='is_in_shopping_cart',
    )

    def get_is_favorited(self, queryset, name, value):
        return queryset.filter(favorite__user=self.request.user)

    def get_is_in_shopping_cart(self, queryset, name, value):
        return queryset.filter(shopping_cart__user=self.request.user)

    class Meta:
        model = Recipe
        fields = ('author', 'tags', 'is_favorited', 'is_in_shopping_cart')


class IngredientFilter(FilterSet):
    name = CharFilter(
        field_name='name',
        lookup_expr='istartswith'
    )

    class Meta:
        model = Ingredient
        fields = ('name', )
