from django.urls import include, path
from djoser.views import TokenCreateView, TokenDestroyView
from rest_framework.routers import DefaultRouter

from .views import CustomUserViewSet

router = DefaultRouter()
router.register('users', CustomUserViewSet)


urlpatterns = [
    path('', include(router.urls)),
    path('auth/token/login/', TokenCreateView.as_view(), name='token_create'),
    path('auth/token/logout/',
         TokenDestroyView.as_view(), name='token_destroy'),
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
]
