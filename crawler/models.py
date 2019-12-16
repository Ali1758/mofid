from django.db import models
from django.conf import settings
from django.urls import reverse
from django.utils.text import slugify
from users.models import User


class Storage(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100)
    complete = models.BooleanField(default=False)
    starter = models.ForeignKey(User, on_delete=models.CASCADE)
    start = models.DateTimeField(auto_now_add=True)
    final = models.DateTimeField(auto_now=True)
    address = models.FilePathField(path=settings.MEDIA_ROOT)
    percentage = models.DecimalField(max_digits=5, decimal_places=0, default=0.00)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Storage, self).save()

    class Meta:
        ordering = ('-start',)
        db_table = 'storage'

    def __str__(self):
        return "{}".format(self.name)

    def download_link(self):
        return reverse("download_item", args=[self.slug])

    def have_backup(self):
        if self.backup_set:
            return True
        return False

    def backups_links(self):
        return reverse("backups", args=[self.slug])
