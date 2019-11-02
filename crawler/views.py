#!/usr/bin/python
# -*- coding: utf-8 -*-
from django.shortcuts import get_object_or_404
from django.http.response import HttpResponse
from .models import Storage
from django.conf import settings
from django.contrib.auth.decorators import login_required
from .tasks import crawler
from django.contrib import messages
from django.shortcuts import redirect


@login_required()
def download_view(request, name):
    output = get_object_or_404(Storage, name__exact=name)
    path = settings.MEDIA_ROOT + output.address
    file = open(path, 'rb')
    response = HttpResponse(file, content_type='application/vnd.ms-excel')
    response['Content-Disposition'] = "attachment; filename={}".format(output.name)
    return response


@login_required()
def full_crawling(request):
    crawler()
    messages.success(request, "فرآیند آغاز شد")
    return redirect('index')


@login_required()
def custom_crawling(request):
    return None
