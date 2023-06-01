from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator
from django.contrib.auth import get_user_model
from drf_extra_fields.fields import Base64ImageField
from users.models import Subscription
from users.serializers import UserListSerializer
from recipes.models import Ingredient, Recipe, Tag, IngredientAmount


User = get_user_model()


class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient,
        fields = '__all__'


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag,
        fields = '__all__'


class RecipeIngredientSerializer(serializers.ModelSerializer):
    recipe = serializers.PrimaryKeyRelatedField(read_only=True)
    amount = serializers.IntegerField(min_value=1, write_only=True,)
    id = serializers.PrimaryKeyRelatedField(
        queryset=Ingredient.objects.all(),
        source='ingredient',)

    class Meta:
        model = IngredientAmount
        fields = ('recipe', 'amount', 'id',)


class RecipeSerializer(serializers.ModelSerializer):
    tags = serializers.PrimaryKeyRelatedField(queryset=Tag.objects.all(),
                                              many=True)
    ingredients = RecipeIngredientSerializer(many=True)
    author = UserListSerializer(read_only=True)
    image = Base64ImageField(use_url=True)
    cooking_time = serializers.IntegerField(min_value=1)

    class Meta:
        model = Recipe
        fields = (
            'id', 'name', 'text', 'author', 'ingredients', 'tags', 'image',
            'cooking_time',)

    def create(self, validated_data):
        ingredients_data = validated_data.pop('ingredients')
        tags_data = validated_data.pop('tags')
        recipe = Recipe.objects.create(**validated_data)
        recipe.tags.set(tags_data)
        self.create_update(recipe, ingredients_data, IngredientAmount,)
        return recipe

    def update(self, instance, validated_data):
        if 'tags' in self.validated_data:
            tags_data = validated_data.pop('tags')
            instance.tags.set(tags_data)
        if 'ingredients' in self.validated_data:
            ingredients_data = validated_data.pop('ingredients')
            quantity = IngredientAmount.objects.filter(
                recipe_id=instance.id)
            quantity.delete()
            self.create_update(ingredients_data, instance, IngredientAmount,)
        return super().update(instance, validated_data)

    def create_update(self, datas, model, recipe):
        create_data = (model(recipe=recipe, amount=data['amount'],
                             ingredient=data['ingredient'],) for data in datas)
        model.objects.bulk_create(create_data)

    def to_representation(self, instance):
        self.fields.pop('tags')
        self.fields.pop('ingredients')
        represent = super().to_representation(instance)
        represent['ingredients'] = GetIngredientSerializer(
            IngredientAmount.objects.filter(recipe=instance),
            many=True).data
        represent['tags'] = TagSerializer(instance.tags, many=True).data
        return represent

    def validate(self, data):
        ingredients = self.initial_data.get('ingredients')
        ingredients_list = [ingredient['id'] for ingredient in ingredients]
        if len(ingredients_list) != len(set(ingredients_list)):
            raise serializers.ValidationError(
                'Ингредиент указан несколько раз')
        return data


class GetIngredientSerializer(serializers.ModelSerializer):
    name = serializers.ReadOnlyField(source='ingredient.name')
    id = serializers.ReadOnlyField(source='ingredient.id')
    measurement_unit = serializers.ReadOnlyField(
        source='ingredient.measurement_unit')

    class Meta:
        model = IngredientAmount
        fields = ('name', 'id', 'measurement_unit', 'amount',)
        validators = [
            UniqueTogetherValidator(queryset=IngredientAmount.objects.all(),
                                    fields=['ingredient', 'recipe'])
        ]


class GetRecipeSerializer(serializers.ModelSerializer):
    author = UserListSerializer(read_only=True)
    tags = TagSerializer(read_only=True, many=True)
    ingredients = serializers.SerializerMethodField()
    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()
    image = Base64ImageField(use_url=True)

    class Meta:
        model = Recipe
        fields = ('name', 'id', 'text', 'is_in_shopping_cart', 'ingredients',
                  'is_favorited', 'tags', 'author', 'cooking_time', 'image', )

    def get_ingredients(self, obj):
        ingredients = IngredientAmount.objects.filter(recipe=obj)
        return GetIngredientSerializer(ingredients, many=True).data

    def get_is_in_shopping_cart(self, obj):
        user = self.context['request'].user
        if user.is_authenticated:
            return obj.cart.filter(user=user).exists()
        return False

    def get_is_favorited(self, obj):
        user = self.context['request'].user
        if user.is_authenticated:
            return obj.favorites.filter(user=user).exists()
        return False


class RecipeSubscribeSerializer(serializers.ModelSerializer):
    image = Base64ImageField()

    class Meta:
        model = Recipe
        fields = ('name', 'cooking_time', 'id', 'image',)


class SubscriptionSerializer(serializers.ModelSerializer):
    first_name = serializers.ReadOnlyField(source='author.first_name')
    username = serializers.ReadOnlyField(source='author.username')
    last_name = serializers.ReadOnlyField(source='author.last_name')
    email = serializers.ReadOnlyField(source='author.email')
    is_subscribed = serializers.SerializerMethodField()
    recipes_count = serializers.ReadOnlyField(source='author.recipes.count')
    recipes = serializers.SerializerMethodField()
    id = serializers.ReadOnlyField(source='author.id')

    class Meta:
        model = Subscription
        fields = (
            'first_name', 'username', 'last_name', 'email',
            'is_subscribed', 'recipes_count', 'recipes', 'id',)

    def get_recipes(self, obj):
        queryset = Recipe.objects.filter(author=obj.author)
        request = self.context.get('request')
        limit = request.GET.get('recipes_limit')
        if limit:
            queryset = queryset[:int(limit)]
        return RecipeSubscribeSerializer(queryset, many=True).data

    def get_is_subscribed(self, obj):
        return Subscription.objects.filter(author=obj.author, user=obj.user,
                                           ).exists()
