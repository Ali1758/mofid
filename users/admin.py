from django.contrib import admin
from .models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    fields = ('first_name', 'last_name', 'telegram_user', 'accessibility')
    actions = ['access_accept']

    def access_accept(self, request, queryset):
        queryset.update(accessibility=True)
    access_accept.short_description = 'Accept accessibility of selected Users.'
