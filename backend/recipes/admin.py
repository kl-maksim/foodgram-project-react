from django.contrib import admin

from .models import (Ingredient, Recipe, Favorite, Recipeingredients,
                     ShoppingCart, Tag)


class IngredientAdmin(admin.ModelAdmin):
    list_filter = ('name',)
    search_fields = ('name', 'measurement_unit',)
    list_display = ('name', 'measurement_unit', 'id',)
    empty_value_display = 'empty'


class RecipeingredientsAdmin(admin.ModelAdmin):
    list_filter = ('ingredient', 'recipe',)
    search_fields = ('ingredient', 'recipe',)
    list_display = ('ingredient', 'recipe', 'amount', 'id',)
    empty_value_display = 'empty'


class RecipeIngredientsInLine(admin.TabularInline):
    model = Recipe.ingredients.through
    extra = 1
    min_num = 1


class RecipeAdmin(admin.ModelAdmin):
    list_filter = ('name', 'author', 'tags',)
    search_fields = ('name', 'author', 'ingredients', 'tags', 'cooking_time',)
    list_display = ('name', 'text', 'author', 'pub_date', 'cooking_time',
                    'count_favor', 'id',)
    empty_value_display = 'empty'
    inlines = (RecipeIngredientsInLine,)

    def count_favor(self, obj):
        return obj.favorites.count()


class TagAdmin(admin.ModelAdmin):
    list_filter = ('name', 'slug',)
    search_fields = ('name', 'slug')
    list_display = ('name', 'slug', 'color', 'id',)
    empty_value_display = 'empty'


class ShoppingCartAdmin(admin.ModelAdmin):
    list_filter = ('user', 'recipe',)
    search_fields = ('user', 'recipe',)
    list_display = ('user', 'recipe', 'id',)
    empty_value_display = 'empty'


class FavoriteAdmin(admin.ModelAdmin):
    list_filter = ('user', 'recipe',)
    search_fields = ('user', 'recipe',)
    list_display = ('user', 'recipe', 'id',)
    empty_value_display = 'empty'


admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(Recipeingredients, RecipeingredientsAdmin)
admin.site.register(Recipe, RecipeAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(ShoppingCart, ShoppingCartAdmin)
admin.site.register(Favorite, FavoriteAdmin)
