from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

User = get_user_model()


class Ingredient(models.Model):
    """Модель ингредиентов."""
    name = models.CharField(
        max_length=150
    )
    measurement_unit = models.CharField(max_length=20)

    class Meta:
        verbose_name_plural = 'Ингредиенты'

    def __str__(self):
        return f'{self.name}: {self.measurement_unit}'


class Tag(models.Model):
    """Модель тегов."""
    name = models.CharField(
        max_length=150,
        help_text='Название тега'
    )
    color = models.CharField(
        max_length=7,
        verbose_name='Цветовой HEX-код'
    )
    slug = models.SlugField(
        max_length=100,
        unique=True
    )

    class Meta:
        verbose_name_plural = 'Теги'

    def __str__(self):
        return self.name


class Recipe(models.Model):
    """Модель рецептов"""
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='recipe',
        verbose_name='Автор',
    )
    name = models.CharField(
        max_length=100,
        help_text='Название рецепта',
    )
    image = models.ImageField(
        upload_to='recipe/',
        blank=True,
        null=True,
        default=None
    )
    text = models.TextField(
        'Описание',
        help_text='Описание рецепта'
    )
    ingredients = models.ManyToManyField(
        Ingredient,
        through='Recipeingredients',
    )
    tags = models.ManyToManyField(
        Tag,
        through='RecipeTag',
    )

    cooking_time = models.PositiveIntegerField(
        default=0,
        verbose_name='Время приготовления в минутах'
    )
    pub_date = models.DateTimeField(
        'Дата публикации',
        auto_now_add=True
    )

    def get_ingredients(self):
        return "\n".join([ingr.ingredients for ingr in self.product.all()])

    class Meta:
        ordering = ['-pub_date']
        verbose_name_plural = 'Рецепты'

    def __str__(self):
        return self.name


class Recipeingredients(models.Model):
    """Связная модель репет-ингредиент"""
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='recipeingredients1'
    )
    ingredients = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
        related_name='recipeingredients2'
    )
    amount = models.IntegerField(
        validators=[
            MinValueValidator(
                1,
                message='Кол-во не меньше 1'
            ),
            MaxValueValidator(
                10000,
                message='Кол-во не больше 10000'
            )
        ],
    )

    class Meta:
        verbose_name_plural = 'репет-ингредиент'

    def __str__(self):
        return f'{self.recipe} {self.ingredients}'


class RecipeTag(models.Model):
    """Связная модель тег-ингредиент"""
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE
    )
    tag = models.ForeignKey(
        Tag,
        on_delete=models.CASCADE
    )

    class Meta:
        verbose_name_plural = 'репет-тег'

    def __str__(self):
        return f'{self.recipe} {self.tag}'


class RecipesFavorites(models.Model):
    """Модель избранных рецептов"""
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='favorite',
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='favorite',
    )

    class Meta:
        verbose_name_plural = 'Избранные рецепты'

    def __str__(self):
        return f'Ползьователь: {self.user} подписался на рецепт: {self.recipe}'


class ShoppingCart(models.Model):
    """Модель список покупок"""
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='shopping_cart',
        verbose_name='Пользователь',
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='shopping_cart',
        verbose_name='Рецепт',
    )

    class Meta:
        verbose_name = 'Список покупок'
        verbose_name_plural = 'Списки покупок'
        constraints = [
            models.UniqueConstraint(fields=['user', 'recipe'],
                                    name='unique_shopping_cart')
        ]

    def __str__(self):
        return f'{self.user} добавил в список покупок: {self.recipe}'
