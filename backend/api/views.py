from django.db.models import Sum
from django.http.response import HttpResponse
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .filters import NameSearchFilter, RecipeFilter
from .mixins import ViewSetMixin
from .pagination import CustomPagination
from .permissions import IsAuthorOrReadOnly
from .serializers import (GetRecipeSerializer, IngredientSerializer,
                          RecipeSerializer, RecipeSubscribeSerializer,
                          TagSerializer)
from recipes.models import (Favorite, Ingredient, Recipe, Recipeingredients,
                            ShoppingCart, Tag)


class IngredientViewSet(ViewSetMixin):
    serializer_class = IngredientSerializer
    queryset = Ingredient.objects.all()
    permission_classes = (permissions.AllowAny,)
    filter_backends = (NameSearchFilter,)
    search_fields = ('^name',)
    pagination_class = None


class TagViewSet(ViewSetMixin):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = (permissions.AllowAny,)
    pagination_class = None


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    filter_backends = (DjangoFilterBackend,)
    filterset_class = RecipeFilter
    pagination_class = CustomPagination
    serializer_class = RecipeSerializer

    def get_queryset(self):
        is_favorited = self.request.query_params.get('is_favorited')
        is_in_shopping_cart = self.request.query_params.get(
            'is_in_shopping_cart')
        if is_favorited is not None and int(is_favorited) == 1:
            return Recipe.objects.filter(favorites__user=self.request.user)
        if is_in_shopping_cart is not None and int(is_in_shopping_cart) == 1:
            return Recipe.objects.filter(cart__user=self.request.user)
        return Recipe.objects.all()

    def perform_create(self, serializer):
        serializer = RecipeSerializer
        serializer.save(author=self.request.user)

    def perform_update(self, serializer):
        serializer.save(author=self.request.user)

    def destroy(self, request, *args, **kwargs):
        self.perform_destroy(self.get_object())
        return Response({"Вы удалили рецепт"},
                        status=status.HTTP_204_NO_CONTENT)

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return GetRecipeSerializer
        return RecipeSerializer

    def get_permissions(self):
        if self.action != 'create':
            return (IsAuthorOrReadOnly(),)
        return super().get_permissions()

    def post_delete(self, model, request, pk, serializer,):
        if self.request.method == 'POST':
            recipe = get_object_or_404(Recipe, pk=pk,)
            model.objects.get_or_create(recipe=recipe, user=request.user,)
            return Response(serializer(recipe).data,
                            status=status.HTTP_201_CREATED)
        if self.request.method == 'DELETE':
            recipe = get_object_or_404(Recipe, pk=pk,)
            if model.objects.filter(recipe=recipe, user=request.user,
                                    ).exists():
                data = get_object_or_404(model, recipe=recipe,
                                         user=request.user,)
                data.delete()
                return Response({"Рецепт был удален"},
                                status=status.HTTP_204_NO_CONTENT)
            return Response(
                {"Рецепта нет в избранном списке покупок"},
                status=status.HTTP_400_BAD_REQUEST)
        return 'Метод запроса не соответсвует ["POST", "DELETE"]'

    @action(detail=False, methods=('GET',),
            permission_classes=[permissions.IsAuthenticated, ])
    def download_shopping_cart(self, request):
        user = request.user
        now = timezone.now()
        filename = f'{user.username}_shopping_list.txt'
        shopping_list = [
            f'Список покупок для: {user.username}\n\n'
            f'Дата: {now:%Y-%m-%d}\n\n'
        ]
        ingredients = Recipeingredients.objects.filter(
            recipe__cart__user=user).values('ingredient__name',
                                            'ingredient__measurement_unit'
                                            ).annotate(
            ingredient_amount=Sum('amount'))

        for ing in ingredients:
            shopping_list.append(
                f'{ing["ingredient__name"]}: {ing["ingredient_amount"]} '
                f'{ing["ingredient__measurement_unit"]}'
            )
        response = HttpResponse(
            shopping_list, content_type='text.txt; charset=utf-8'
        )
        response['Content-Disposition'] = f'attachment; filename={filename}'
        return response

    @action(detail=True, methods=['POST', 'DELETE'])
    def shopping_cart(self, request, pk,):
        serializer = RecipeSubscribeSerializer
        model = ShoppingCart
        return self.post_delete(model, request, pk, serializer,)

    @action(detail=True, methods=['POST', 'DELETE'])
    def favorite(self, request, pk,):
        serializer = RecipeSubscribeSerializer
        model = Favorite
        return self.post_delete(model, request, pk, serializer,)
