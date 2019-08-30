from django.contrib import admin
from .models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    fields = ('first_name', 'last_name', 'username', 'telegram_id', 'accessibility')
    list_display = ('__str__', 'telegram_id', 'accessibility')
    actions = ['access_accept']

    def access_accept(self, request, queryset):
        queryset.update(accessibility=True)
    access_accept.short_description = 'Accept accessibility of selected Users.'
