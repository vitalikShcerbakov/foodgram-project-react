from django.db.models import F, Sum
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from api.serializers import (IngredientSerializer, RecipeReadSerializer,
                             RecipesFavoritesSerializer, RecipeShortSerializer,
                             RecipeWriteSerializer, ShoppingCartSerializer,
                             TagSerializer)
from recipe.models import (Ingredient, Recipe, Recipeingredients,
                           RecipesFavorites, ShoppingCart, Tag)

from .filters import FilterRecipe, IngredientFilter


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = TagSerializer
    queryset = Tag.objects.all()
    pagination_class = None


class IngredientViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    pagination_class = None
    filter_backends = (DjangoFilterBackend, )
    filterset_class = IngredientFilter
    search_fields = ('name', )


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    filter_backends = (DjangoFilterBackend, )
    filterset_class = FilterRecipe
    search_fields = ('name', )

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def get_serializer_class(self):
        if self.action in ('create', 'partial_update'):
            return RecipeWriteSerializer
        return RecipeReadSerializer

    @action(
        detail=False,
        methods=['GET'],
        url_path='download_shopping_cart',
        pagination_class=None)
    def download_shopping_cart(self, request):
        ingredients = Recipeingredients.objects.filter(
            recipe__shopping_cart__user=request.user).values_list(
            'ingredients__name', 'amount', 'ingredients__measurement_unit')
        ingredients = ingredients.values(
            'ingredients__name', 'ingredients__measurement_unit'
        ).annotate(
            name=F('ingredients__name'),
            units=F('ingredients__measurement_unit'),
            total=Sum('amount'),
        ).order_by('-total')
        text = '\n'.join([
            f'{ingredient["name"]} {ingredient["units"]} {ingredient["total"]}'
            for ingredient in ingredients
        ])
        response = HttpResponse(text, content_type='text/plain')
        response['Content-Disposition'] = (
            'attachment; filename="shopping_cart.txt"')
        return response

    @action(
        detail=True,
        methods=['POST', 'DELETE'],
        url_path='shopping_cart',
        url_name='shopping_cart',
        pagination_class=None)
    def shopping_cart(self, request, pk):
        recipe = get_object_or_404(Recipe, pk=pk)
        if request.method == 'POST':
            serializer = ShoppingCartSerializer(
                data={'user': request.user.id, 'recipe': recipe.id}
            )
            serializer.is_valid(raise_exception=True)
            serializer.save()

            shopping_cart = RecipeShortSerializer(recipe)
            return Response(
                shopping_cart.data, status=status.HTTP_201_CREATED
            )
        shopping_cart_recipe = get_object_or_404(
            ShoppingCart, user=request.user, recipe=recipe
        )
        shopping_cart_recipe.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(
        detail=True,
        methods=['POST', 'DELETE'],
        url_path='favorite',
        url_name='favorite',
        pagination_class=None)
    def favorite(self, request, pk):
        recipe = get_object_or_404(Recipe, pk=pk)
        print(recipe.id)
        if request.method == 'POST':
            serializer = RecipesFavoritesSerializer(
                data={'user': request.user.id, 'recipe': recipe.id}
            )
            serializer.is_valid(raise_exception=True)
            serializer.save()

            favorite = RecipeShortSerializer(recipe)
            return Response(
                favorite.data, status=status.HTTP_201_CREATED
            )
        shopping_cart_recipe = get_object_or_404(
            RecipesFavorites, user=request.user, recipe=recipe
        )
        shopping_cart_recipe.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
