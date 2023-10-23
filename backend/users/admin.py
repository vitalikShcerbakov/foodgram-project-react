from django.contrib import admin
from django.contrib.auth.models import Group
from recipe.models import ShoppingCart
from rest_framework.authtoken.models import TokenProxy


from .models import Follow, User


admin.site.unregister(TokenProxy)
admin.site.unregister(Group)


class ShoppingCartInline(admin.TabularInline):
    model = ShoppingCart
    extra = 1


class FollowInline(admin.TabularInline):
    fk_name = "user"
    model = Follow
    extra = 1


@admin.register(Follow)
class FollowAdmin(admin.ModelAdmin):
    pass


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    fields = ('username', 'email', 'first_name', 'last_name')
    list_filter = ('email', 'username')
    search_fields = ('email', 'username')
    inlines = [FollowInline, ShoppingCartInline]
