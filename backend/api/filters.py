from django.contrib.auth import get_user_model
import django_filters
# from rest_framework.filters import SearchFilter

from recipes.models import Tag, Recipe, Ingredient

User = get_user_model()


class RecipeFilter(django_filters.FilterSet):
    author = django_filters.ModelChoiceFilter(queryset=User.objects.all()),

    tags = django_filters.ModelMultipleChoiceFilter(field_name='tags__slug',
                                                    to_field_name='slug',
                                                    queryset=Tag.objects.all())

    class Meta:
        model = Recipe
        fields = ('author', 'tags',)


class IngredientFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(field_name='name',
                                     lookup_expr='istartswith',)

    class Meta:
        model = Ingredient
        fields = ('name',)
