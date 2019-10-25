from django.db import models
from django.contrib.auth.models import AbstractUser, UserManager


class UserAccessManager(models.Manager):
    def get_queryset(self):
        return super(UserAccessManager, self).get_queryset().filter(accessibility=True)


class User(AbstractUser):
    accessibility = models.BooleanField(default=False)
    telegram_id = models.IntegerField()

    objects = UserManager()
    access = UserAccessManager()

    def __str__(self):
        return '{} - {}'.format(self.first_name, self.last_name)
