from django.contrib import admin
from .models import Storage, Backup


class BackupInline(admin.TabularInline):
    model = Backup
    exclude = ('created',)


@admin.register(Storage)
class StorageAdmin(admin.ModelAdmin):
    list_display = ('name', 'start', 'complete')
    inlines = [BackupInline]


admin.site.register(Backup)
