from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    accessibility = models.BooleanField(default=False)
    telegram_user = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return '{} - {}'.format(self.first_name, self.last_name)

