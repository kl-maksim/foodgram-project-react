from django.contrib.auth import get_user_model
from djoser.views import UserViewSet
from rest_framework import permissions, status
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response

from .models import Follow
from api.pagination import CustomPagination
from api.serializers import SubscriptionSerializer

User = get_user_model()


class UserViewSet(UserViewSet):
    pagination_class = CustomPagination

    @action(permission_classes=[permissions.IsAuthenticated],
            methods=['GET'],
            detail=False,)
    def subscriptions(self, request):
        queryset = self.paginate_queryset(
            self.request.user.follower.all())
        serializer = SubscriptionSerializer(queryset,
                                            many=True,
                                            context={'request': request}).data
        return self.get_paginated_response(serializer)

    @action(permission_classes=[permissions.IsAuthenticated],
            methods=['POST', 'DELETE'],
            detail=True,
            )
    def subscribe(self, request, id=None):
        user = request.user
        author = get_object_or_404(User, id=id)
        sub = Follow.objects.filter(user=user, author=author,)
        if self.request.method == 'POST':
            if user == author:
                return Response({'Вы не можете подписаться на самого себя'},
                                status=status.HTTP_400_BAD_REQUEST,)
            if sub.exists():
                return Response({'Вы уже подписаны'},
                                status=status.HTTP_400_BAD_REQUEST,)
            serializer = SubscriptionSerializer(
                Follow.objects.create(user=user, author=author,),
                context={'request': request}).data
            return Response(serializer, status=status.HTTP_201_CREATED,)
        if sub.exists():
            obj = get_object_or_404(Follow, user=user,
                                    author=author,)
            obj.delete()
            return Response({'Вы отписались от рассылки'},
                            status=status.HTTP_204_NO_CONTENT)
        if user == author:
            return Response({'Вы не можете отписаться от себя'},
                            status=status.HTTP_204_NO_CONTENT)
        return Response({'Вы не подписаны'},
                        status=status.HTTP_400_BAD_REQUEST)
