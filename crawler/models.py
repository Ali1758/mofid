from django.db import models
from django.conf import settings
from django.urls import reverse


class Storage(models.Model):
    name = models.CharField(max_length=25)
    complete = models.BooleanField(default=False)
    start = models.DateTimeField(auto_created=True)
    final = models.DateTimeField(auto_now=True)
    address = models.FilePathField(path=settings.MEDIA_ROOT)

    class Meta:
        ordering = ('-start',)

    def __str__(self):
        return "{} - {}".format(self.name, self.start)

    def download_link(self):
        reverse("download", args=[self.name])
