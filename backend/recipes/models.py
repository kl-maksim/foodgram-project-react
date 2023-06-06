from django.core.validators import MinValueValidator
from django.db import models
from django.contrib.auth import get_user_model
from foodgram import settings

User = get_user_model()


class Tag(models.Model):
    name = models.CharField('Название тега',
                            max_length=200,
                            unique=True,)
    slug = models.SlugField('slug',
                            max_length=200,
                            unique=True)
    color = models.CharField('Цвет',
                             max_length=7,
                             default='#FF0000',
                             unique=True,)

    class Meta:
        verbose_name = 'Тег'
        ordering = ('name',)

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    name = models.CharField('Название ингредиента',
                            max_length=200,)
    measurement_unit = models.CharField('Единицы измерения',
                                        max_length=200,)

    class Meta:
        verbose_name = 'Ингредиент'
        ordering = ('name', )

    def __str__(self):
        return self.name


class Recipe(models.Model):
    name = models.CharField('Название рецепта',
                            max_length=200)
    author = models.ForeignKey(User,
                               on_delete=models.CASCADE,
                               verbose_name='Автор рецепта',
                               related_name='recipes',)
    text = models.TextField('Описание рецепта',)
    image = models.ImageField('Изображение',)
    tags = models.ManyToManyField(Tag,
                                  related_name='recipes',
                                  verbose_name='Теги',)
    ingredients = models.ManyToManyField(Ingredient,
                                         related_name='recipes',
                                         verbose_name='Ингредиенты',
                                         through='Recipeingredients',)
    pub_date = models.DateTimeField('Дата публикации',
                                    auto_now_add=True,
                                    db_index=True,)
    cooking_time = models.PositiveIntegerField(
        verbose_name='Время приготовления рецепта, указанное в минутах',
        validators=[MinValueValidator(settings.VALID_COUNT)],)

    class Meta:
        verbose_name = 'Рецепт'
        ordering = ('pub_date',)
        constraints = [
            models.UniqueConstraint(
                name='unique_author_name',
                fields=['author', 'name'],)]

    def __str__(self):
        return f'Рецепт {self.name}'


class Recipeingredients(models.Model):
    ingredient = models.ForeignKey(Ingredient,
                                   related_name='recipeingredients',
                                   verbose_name='Ингридиент',
                                   on_delete=models.CASCADE,)
    recipe = models.ForeignKey(Recipe,
                               related_name='recipeingredients',
                               verbose_name='Рецепт',
                               on_delete=models.CASCADE,)
    amount = models.PositiveSmallIntegerField(
        verbose_name='Количество используемого ингредиента',
        validators=[MinValueValidator(settings.VALID_COUNT)])

    class Meta:
        ordering = ('-id', )
        verbose_name = 'Количество используемого ингредиента'
        constraints = [
            models.UniqueConstraint(
                name='recipes_ingredients',
                fields=['ingredient', 'recipe', ],)]

    def __str__(self):
        return f'{self.recipe}'


class Favorite(models.Model):
    user = models.ForeignKey(User,
                             related_name='favorites',
                             verbose_name='Пользователь',
                             on_delete=models.CASCADE,)
    recipe = models.ForeignKey(Recipe,
                               related_name='favorites',
                               verbose_name='Избранный рецепт',
                               on_delete=models.CASCADE,)

    class Meta:
        verbose_name = 'Добавление рецепта в избранное'
        ordering = ['id', ]
        constraints = [
            models.UniqueConstraint(
                name='unique_user_recipe',
                fields=['user', 'recipe', ],)]

    def __str__(self):
        return f'{self.user} добавил в избранное {self.recipe}'


class ShoppingCart(models.Model):
    recipe = models.ForeignKey(Recipe,
                               related_name='cart',
                               verbose_name='Список рецептов',
                               on_delete=models.CASCADE,)
    user = models.ForeignKey(User,
                             related_name='cart',
                             verbose_name='Пользователь',
                             on_delete=models.CASCADE,)

    class Meta:
        verbose_name = 'Добавление рецепта в список покупок'
        ordering = ('pk',)
        constraints = [
            models.UniqueConstraint(
                name='shopping_user_recipe',
                fields=['user', 'recipe', ],)]

    def __str__(self):
        return f'{self.user}, {self.recipe}'
