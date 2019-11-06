from django.shortcuts import render, redirect, get_object_or_404
from django.http.response import HttpResponse
from .models import Storage
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .crawler import crawler_engine
from jdatetime import datetime


@login_required()
def download_items(request, slug):
    output = get_object_or_404(Storage, slug__exact=slug)
    path = settings.MEDIA_ROOT + output.address
    file = open(path, 'rb')
    response = HttpResponse(file, content_type='application/vnd.ms-excel')
    response['Content-Disposition'] = "attachment; filename={}".format(output.name)
    return response


@login_required()
def full_crawling(request):
    output_name = "Output_{}".format(str(datetime.now()).split('.')[-2])
    output_path = output_name + '.xlsx'
    s = Storage(name=output_name, complete=False, address=output_path)
    s.save()
    crawler_engine.delay(output_name)
    messages.success(request, "فرآیند آغاز شد")
    return redirect('index')


@login_required()
def custom_crawling(request):
    return None
