from django.shortcuts import render, redirect, get_object_or_404
from django.http.response import HttpResponse
from .models import Storage
from django.conf import settings
from django.contrib.auth.decorators import login_required


@login_required()
def download_view(request):
    return render(request, "download.html", {"items": Storage.objects.all()})


@login_required()
def download_items(request, slug):
    output = get_object_or_404(Storage, slug__exact=slug)
    path = settings.MEDIA_ROOT + output.address
    file = open(path, 'rb')
    response = HttpResponse(file, content_type='application/vnd.ms-excel')
    response['Content-Disposition'] = "attachment; filename={}".format(output.name)
    return response
