from django.db import models
from django.conf import settings
from django.urls import reverse
from django.utils.text import slugify


class Storage(models.Model):
    name = models.CharField(max_length=25)
    complete = models.BooleanField(default=False)
    start = models.DateTimeField(auto_now_add=True)
    final = models.DateTimeField(auto_now=True)
    address = models.FilePathField(path=settings.MEDIA_ROOT)
    percentage = models.DecimalField(max_digits=5, decimal_places=0, default=0.00)

    class Meta:
        ordering = ('-start',)
        db_table = 'storage'

    def __str__(self):
        return "{}".format(self.name)

    def download_link(self):
        return reverse("download", args=[slugify(self.name)])
