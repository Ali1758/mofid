from django.shortcuts import render, get_object_or_404
from django.http.response import HttpResponse
from .models import Storage, Backup
from django.conf import settings
from django.contrib.auth.decorators import login_required


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
    response['Content-Disposition'] = "attachment; filename={}".format(output.name)
    return response


@login_required(login_url="Login")
def download_backup(request, slug):
    output = get_object_or_404(Backup, name__exact=slug)
    path = settings.MEDIA_ROOT + output.address
    file = open(path, 'rb')
    response = HttpResponse(file, content_type='application/vnd.ms-excel')
    response['Content-Disposition'] = "attachment; filename={}".format(output.name)
    return response
