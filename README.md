## Проект Foodgram - "Продуктовый помощник"

![example branch parameter](https://github.com/kl-maksim/foodgram-project-react/actions/workflows/foodgram_workflow.yml/badge.svg?branch=master)

### Описание проекта Foodgram 

**Это сервис, на котором пользователи могут:**

- Публиковать свои рецепты;
- Добавлять понравившиеся рецепты в список «Избранное»;
- Подписываться на публикации других пользователей;
- Скачивать сводный список продуктов, необходимых для приготовления блюд. 

### В проекте реализованы различные пользовательские роли:

**Неавторизованный пользователь:**

- Имеет возможность пройти регистрацию и создать аккаунт;
- Просматривать рецепты на главной;
- Просматривать отдельные страницы рецептов;
- Просматривать страницы пользователей;
- Фильтровать рецепты по тегам.

**Авторизованный пользователь:**

- Авторизироваться в системе под своим логином и паролем;
- Менять пароль;
- Выходить из системы;
- Создавать, редактировать и удалять собственные рецепты;
- Просматривать страницы отдельных рецептов;
- Просматривать страницы пользователей;
- Просматривать рецепты на главной странице;
- Фильтровать рецепты по тегам;
- Работать с персональным списком избранного;
- Работать с персональным списком покупок: добавлять/удалять **любые** рецепты, выгружать файл с количеством необходимых ингредиентов для рецептов из списка покупок;
- Подписываться на публикации авторов рецептов и отменять подписку, просматривать свою страницу подписок.

**Администратор:**

Администратор обладает всеми правами авторизованного пользователя. 

Помимо всех прав авторизированного пользователя, **администратор** имеет возможность:
- Добавлять, удалять и редактировать ингредиенты;
- Добавлять, удалять и редактировать теги;
- Редактировать и удалять **любые из существующих на платформе рецептов** рецепты;
- Изменять пароль любого пользователя;
- Создавать, блокировать и удалять аккаунты пользователей.


### Инструкция по установке проекта ```Foodgram```:

- Клонировать репозиторий командой в терминале:
```git clone git@github.com:kl-maksim/foodgram-project-react.git```
- Перейти в директорию ```infra``` следующей командой:
```cd infra```
- Собрать контейнеры командой:
```docker-compose up -d```
- После необходимо перейти в контейнер ```backend``` и выполнить следующие команды:
```docker-compose exec backend python manage.py migrate```
```docker-compose exec backend python manage.py collectstatic --no-input```
- для создания супер пользомателя можно использовать команду:
```docker-compose exec backend python manage.py createsuperuser```

### Адреса для проверки проекта:

- http://158.160.104.41/admin Админка проекта
- http://158.160.104.41/signin Авторизация и регистрация пользователя
- http://158.160.104.41/recipes Главная страница с рецептами
- http://158.160.104.41/recipes/create Создание рецепта
- http://158.160.104.41/favorites Избранные рецепты


### Данную работы выполнил:

Cтудент 50 когорты Клёнов Максим

### Используемые технологии:

- Python
- Django
- DRF
- djoser
- PostgreSQL
- nginx
- gunicorn
- Docker Hub
- Github Actions
- Yandex cloud
