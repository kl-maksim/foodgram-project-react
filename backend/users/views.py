from django.contrib.auth import get_user_model
from djoser.views import UserViewSet
from rest_framework import permissions
from rest_framework.decorators import action

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
