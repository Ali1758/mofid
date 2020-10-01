from django.shortcuts import render, get_object_or_404, redirect
from django.http.response import HttpResponse
from django.conf import settings
from django.contrib.auth.decorators import login_required

from .models import Storage, Backup
from .crawler import crawler_repair


@login_required(login_url="Login")
def download_view(request):
    return render(request, "download.html", {"items": Storage.objects.all()})


@login_required(login_url="Login")
def backups_view(request, slug):
    return render(request, "backup.html", {"file": Storage.objects.get(slug__exact=slug),
                                           "backups": Backup.objects.filter(file__slug__exact=slug)})


@login_required(login_url="Login")
def download_items(request, slug):
    output = get_object_or_404(Storage, slug__exact=slug)
    path = settings.MEDIA_ROOT + output.address
    file = open(path, 'rb')
    response = HttpResponse(file, content_type='application/vnd.ms-excel')
    response['Content-Disposition'] = "attachment; filename={}.xlsx".format(output.name)
    return response


@login_required(login_url="Login")
def download_backup(request, slug):
    output = get_object_or_404(Backup, name__exact=slug)
    path = settings.MEDIA_ROOT + output.address
    file = open(path, 'rb')
    response = HttpResponse(file, content_type='application/vnd.ms-excel')
    response['Content-Disposition'] = "attachment; filename={}.xlsx".format(output.name)
    return response


@login_required(login_url="Login")
def repair_items(request, slug):
    obj = get_object_or_404(Storage, slug__exact=slug)
    obj.complete = False
    obj.percentage = 0
    obj.save()
    crawler_repair.delay(obj)
    return redirect('index')
