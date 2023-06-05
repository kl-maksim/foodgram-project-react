from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    first_name = models.CharField('Имя',
                                  max_length=150,)
    username = models.CharField('Уникальное имя пользователя',
                                max_length=150,
                                unique=True,)
    last_name = models.CharField('Фамилия',
                                 max_length=150,)
    email = models.EmailField('Адрес электронной почты',
                              max_length=254,
                              unique=True,)
    password = models.CharField('Пароль',
                                max_length=150,)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'username', 'last_name', 'password', ]

    class Meta:
        ordering = ['id', ]
        verbose_name = 'Пользователь'
        constraints = [
            models.UniqueConstraint(
                fields=['email', 'username'],
                name='unique_user'
            )
        ]

    def __str__(self):
        return self.username


class Follow(models.Model):
    user = models.ForeignKey(User,
                             related_name='follower',
                             verbose_name='Подписчик',
                             on_delete=models.CASCADE,)
    author = models.ForeignKey(User,
                               related_name='following',
                               verbose_name='Автор',
                               on_delete=models.CASCADE,)

    class Meta:
        ordering = ['id', ]
        verbose_name = 'Подписка'
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'author'],
                name='unique_subscribe'
            )
        ]

    def __str__(self):
        return f'Пользователь {self.user} подписан на {self.author}'
