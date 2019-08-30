from django.db import models
from django.contrib.auth.models import AbstractUser


class UserManager(models.Manager):
    def get_queryset(self):
        return super(UserManager, self).get_queryset().filter(accessibility=True)


class User(AbstractUser):
    accessibility = models.BooleanField(default=False)
    telegram_id = models.IntegerField(max_length=15)

    def __str__(self):
        return '{} - {}'.format(self.first_name, self.last_name)

