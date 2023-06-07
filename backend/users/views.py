from djoser.views import UserViewSet
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import Follow, User
from api.pagination import CustomPagination
from api.serializers import SubscriptionSerializer, UserSerializer


class UserViewSet(UserViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    pagination_class = CustomPagination

    @action(["GET"], detail=False)
    def me(self, request, *args, **kwargs):
        return super().me(request, *args, **kwargs)

    @action(methods=["GET"], detail=False,
            permission_classes=[IsAuthenticated])
    def subscriptions(self, request, *args, **kwargs):
        queryset = User.objects.filter(following__user=self.request.user)
        page = self.paginate_queryset(queryset)
        serializer = SubscriptionSerializer(
            page, many=True, context=self.get_serializer_context()
        )
        return self.get_paginated_response(serializer.data)

    @action(
        methods=["POST", "DELETE"], detail=True,
        permission_classes=[IsAuthenticated]
    )
    def subscribe(self, request, *args, **kwargs):
        user = request.user
        author = get_object_or_404(User, pk=kwargs.get("id"))
        if request.method == "POST":
            serializer = SubscriptionSerializer(
                author, data=request.data,
                context=self.get_serializer_context()
            )
            serializer.is_valid(raise_exception=True)
            Follow.objects.create(user=user, author=author)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        serializer = SubscriptionSerializer(
            author, data=request.data,
            context=self.get_serializer_context()
        )
        serializer.is_valid(raise_exception=True)
        Follow.objects.get(user=user, author=author).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
