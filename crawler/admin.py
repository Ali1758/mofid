from django.contrib import admin
from .models import Storage, Backup


@admin.register(Storage)
class StorageAdmin(admin.ModelAdmin):
    list_display = ('name', 'start', 'complete')


admin.site.register(Backup)
