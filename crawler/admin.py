from django.contrib import admin
from .models import Storage


@admin.register(Storage)
class StorageAdmin(admin.ModelAdmin):
    list_display = ('name', 'start', 'complete')
