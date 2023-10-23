import base64

import webcolors
from django.db import transaction
from django.core.files.base import ContentFile
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from recipe.models import (Ingredient, Recipe, Recipeingredients,
                           RecipesFavorites, ShoppingCart, Tag)
from users.serializers import CustomUserCreateSerializer


class HexNameColor(serializers.Field):

    def to_representation(self, value):
        return value

    def to_internal_value(self, data):
        try:
            data = webcolors.hex_to_name(data)
        except ValueError:
            raise serializers.ValidationError('Для этого цвета нет имени')
        return data


class Base64ImageField(serializers.ImageField):
    def to_internal_value(self, data):
        if isinstance(data, str) and data.startswith('data:image'):
            format, imgstr = data.split(';base64,')
            ext = format.split('/')[-1]
            data = ContentFile(base64.b64decode(imgstr), name='temp.' + ext)
        return super().to_internal_value(data)


class TagSerializer(serializers.ModelSerializer):
    color = HexNameColor()

    class Meta:
        model = Tag
        fields = ('id', 'name', 'color', 'slug', )


class IngredientSerializer(serializers.ModelSerializer):
    """Сериализатор для Ingredient."""
    class Meta:
        model = Ingredient
        fields = ('id', 'name', 'measurement_unit', )


class RecipeingredientsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = ('amount', )


class IngredientWriteSerializer(serializers.Serializer):
    """Сериализатор для Ingredient(only writing)."""
    id = serializers.IntegerField()
    amount = serializers.IntegerField()

    class Meta:
        model = Recipeingredients
        fields = ('id', 'amount', )


class IngredientReadsSerializer(serializers.ModelSerializer):
    """Сериализатор для Ingredient (only reading)."""
    id = serializers.ReadOnlyField(source='ingredients.id')
    name = serializers.ReadOnlyField(source='ingredients.name')
    measurement_unit = serializers.ReadOnlyField(
        source='ingredients.measurement_unit')

    class Meta:
        model = Recipeingredients
        fields = ('id', 'name', 'measurement_unit', 'amount', )


class RecipeReadSerializer(serializers.ModelSerializer):
    """Сериализатор для recipe (only reading)."""
    image = Base64ImageField(required=False, allow_null=True)
    tags = TagSerializer(read_only=True, many=True)
    author = CustomUserCreateSerializer(read_only=True, many=False)
    ingredients = IngredientReadsSerializer(
        many=True,
        source='recipeingredients1', )
    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()

    class Meta:
        model = Recipe
        fields = ('id', 'tags', 'author',
                  'ingredients', 'is_in_shopping_cart',
                  'is_favorited', 'name', 'image',
                  'text', 'cooking_time', )

    def get_is_favorited(self, obj):
        user = self.context['request'].user
        if user.is_anonymous:
            return False
        return RecipesFavorites.objects.filter(user=user, recipe=obj).exists()

    def get_is_in_shopping_cart(self, obj):
        user = self.context['request'].user
        if user.is_anonymous:
            return False
        return ShoppingCart.objects.filter(user=user, recipe=obj).exists()


class RecipeWriteSerializer(serializers.ModelSerializer):
    image = Base64ImageField(required=False, allow_null=True)
    tags = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Tag.objects.all()
    )
    ingredients = IngredientWriteSerializer(
        many=True,
        source='recipeingredients1'
    )

    class Meta:
        model = Recipe
        fields = ('ingredients', 'tags',
                  'image', 'name',
                  'text', 'cooking_time', )

    @transaction.atomic
    def create(self, validated_data):
        ingredients = validated_data.pop('recipeingredients1')
        tags = validated_data.pop('tags')
        recipe = Recipe.objects.create(**validated_data)
        recipe.tags.set(tags)
        for ingredient in ingredients:
            current_ingredients = Ingredient.objects.get(
                id=ingredient.get('id'))
            Recipeingredients.objects.create(
                ingredients=current_ingredients,
                recipe=recipe,
                amount=ingredient["amount"]
            )
        return recipe

    @transaction.atomic
    def update(self, instance, validated_data):
        recipe = instance
        instance.image = validated_data.get('image', instance.image)
        instance.name = validated_data.get('name', instance.name)
        instance.text = validated_data.get('text', instance.name)
        instance.cooking_time = validated_data.get(
            'cooking_time', instance.cooking_time
        )
        instance.tags.clear()
        instance.ingredients.clear()
        tags_data = validated_data.get('tags')
        instance.tags.set(tags_data)
        ingredients_data = validated_data.get('recipeingredients1')
        Recipeingredients.objects.filter(recipe=recipe).delete()
        for ingredient in ingredients_data:
            current_ingredients = Ingredient.objects.get(
                id=ingredient.get('id'))
            Recipeingredients.objects.create(
                ingredients=current_ingredients,
                recipe=recipe,
                amount=ingredient["amount"]
            )
        instance.save()
        return instance


class ShoppingCartSerializer(serializers.ModelSerializer):
    """Cериализатор для покупок"""
    class Meta:
        model = ShoppingCart
        fields = ('user', 'recipe')
        validators = [
            UniqueTogetherValidator(
                queryset=ShoppingCart.objects.all(),
                fields=('user', 'recipe'),
                message='Вы уже добавляли это рецепт в список покупок'
            )
        ]


class RecipeShortSerializer(serializers.ModelSerializer):
    """Сериализатор для компактного отображения рецептов."""

    class Meta:
        model = Recipe
        fields = (
            'id',
            'name',
            'image',
            'cooking_time',
        )


class RecipesFavoritesSerializer(serializers.ModelSerializer):
    class Meta:
        model = RecipesFavorites
        fields = ('user', 'recipe')
        validators = [
            UniqueTogetherValidator(
                queryset=RecipesFavorites.objects.all(),
                fields=('user', 'recipe'),
                message='Вы уже добавляли это рецепт в избранное'
            )
        ]
