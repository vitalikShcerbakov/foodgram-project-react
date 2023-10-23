from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """Mодель пользователя."""
    username = models.CharField(
        max_length=150,
        verbose_name='Имя пользователя',
    )
    email = models.EmailField(
        max_length=254,
        unique=True,
        verbose_name='E-mail',
    )
    first_name = models.CharField(
        'Имя',
        max_length=150,
        blank=True
    )
    last_name = models.CharField(
        'Фамилия',
        max_length=150,
        blank=True
    )
    is_subscribed = models.BooleanField(null=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', ]

    class Meta:
        verbose_name_plural = 'Пользователи'


class Follow(models.Model):
    """Модель подписки."""
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='user',
        verbose_name='подписчик'
    )
    following = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='following',
        verbose_name='автор'
    )

    class Meta:
        verbose_name_plural = 'Подписки'
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'following'],
                name='unique_follow'
            )
        ]

    def __str__(self):
        return f'Пользователь: {self.user} подписан на: {self.following}'
