from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.generics import get_object_or_404
from rest_framework.decorators import action
from djoser.views import UserViewSet
from django.contrib.auth import get_user_model
from api.serializers import SubscriptionSerializer
from api.pagination import CustomPagination
from .models import Subscription

User = get_user_model()


class UserViewSet(UserViewSet):
    pagination_class = CustomPagination

    @action(permission_classes=[permissions.IsAuthenticated],
            methods=['GET'],
            detail=False,)
    def subscriptions(self, request):
        queryset = self.paginate_queryset(
            Subscription.objects.filter(user=request.user))
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
        sub = Subscription.objects.filter(user=user, author=author,)
        if self.request.method == 'POST':
            if user == author:
                return Response({'Вы не можете подписаться на самого себя'},
                                status=status.HTTP_400_BAD_REQUEST,)
            if sub.exists():
                return Response({'Вы уже подписаны'},
                                status=status.HTTP_400_BAD_REQUEST,)
            serializer = SubscriptionSerializer(
                Subscription.objects.create(user=user, author=author,),
                context={'request': request}).data
            return Response(serializer, status=status.HTTP_201_CREATED,)
        if sub.exists():
            obj = get_object_or_404(Subscription, user=user,
                                    author=author,)
            obj.delete()
            return Response({'Вы отписались от рассылки'},
                            status=status.HTTP_204_NO_CONTENT)
        if user == author:
            return Response({'Вы не можете отписаться от себя'},
                            status=status.HTTP_204_NO_CONTENT)
        return Response({'Вы не подписаны'},
                        status=status.HTTP_400_BAD_REQUEST)
