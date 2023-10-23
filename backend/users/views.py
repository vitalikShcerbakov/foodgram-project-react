from django.shortcuts import get_object_or_404
from djoser.views import UserViewSet
from rest_framework import permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Follow, User
from .serializers import (CustomUserCreateSerializer, FollowSerializer,
                          FollowShowSerializer)


class CustomUserViewSet(UserViewSet):
    serializer_class = CustomUserCreateSerializer
    queryset = User.objects.all()
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    @action(
        detail=False,
        methods=['GET'],
        url_path='me',
        permission_classes=(permissions.IsAuthenticated,)
    )
    def me(self, request):
        serializer = self.get_serializer(request.user)
        return Response(serializer.data)

    @action(
        detail=True,
        methods=['POST', 'DELETE'],
        url_path='subscribe',
        url_name='subscribe',
        permission_classes=(permissions.IsAuthenticated,)
    )
    def subscribe(self, request, id):
        following = get_object_or_404(User, pk=id)
        if request.method == 'POST':
            serializer = FollowSerializer(
                data={'user': request.user.id, 'following': following.id}
            )
            serializer.is_valid(raise_exception=True)
            serializer.save()
            author_serializer = FollowShowSerializer(
                following, context={'request': request}
            )
            return Response(
                author_serializer.data, status=status.HTTP_201_CREATED
            )
        subscription = get_object_or_404(
            Follow, user=request.user, following=following
        )
        subscription.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(
        detail=False,
        methods=['GET'],
        url_path='subscriptions',
        url_name='subscriptions',
        permission_classes=(permissions.IsAuthenticated,)
    )
    def get_subscriptions(self, request):
        return self.get_paginated_response(
            FollowShowSerializer(
                self.paginate_queryset(
                    User.objects.filter(following__user=request.user)
                ),
                many=True,
                context={'request': request},
            ).data
        )
