from django.contrib import admin
from .models import User, Follow


class SubscriptionAdmin(admin.ModelAdmin):
    list_filter = ('user', 'author',)
    search_fields = ('user', 'author',)
    list_display = ('id', 'user', 'author',)
    empty_value_display = 'empty'


class UserAdmin(admin.ModelAdmin):
    list_filter = ('first_name', 'email',)
    search_fields = ('first_name', 'username', 'last_name',)
    list_display = ('first_name', 'username', 'last_name',
                    'email', 'password', 'id',)
    empty_value_display = 'empty'


admin.site.register(Follow, SubscriptionAdmin)
admin.site.register(User, UserAdmin)
