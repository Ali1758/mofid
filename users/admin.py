from django.contrib import admin
from .models import User
from django.contrib.auth.admin import UserAdmin
from django import forms
from django.contrib.auth.forms import UserCreationForm


class UserCreation(UserCreationForm):
    accessibility = forms.BooleanField()
    telegram_id = forms.IntegerField()

    class Meta:
        model = User
        fields = ['username', 'accessibility', 'telegram_id']

    def save(self, *args, **kwargs):
        user = super(UserCreation, self).save(commit=False)
        user.telegram_id = self.cleaned_data["telegram_id"]
        user.accessibility = self.cleaned_data["accessibility"]
        # if commit:
        user.save()
        return user


UserAdmin.add_fieldsets = (
    (None, {"classes": ("wide",), "fields": ("username", "password1", "password2", 'accessibility', 'telegram_id')},),
)
UserAdmin.add_form = UserCreation

UserAdmin.fieldsets = (
    (None, {'fields': ('username', 'password')}),
    ('Personal info', {'fields': ('first_name', 'last_name', 'email')}),
    ('Permissions', {
        'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
    }),
    (None, {"classes": ("wide",), "fields": ('accessibility', 'telegram_id')},),
)

admin.site.register(User, UserAdmin)
