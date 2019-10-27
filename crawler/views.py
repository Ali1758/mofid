#!/usr/bin/python
# -*- coding: utf-8 -*-

from django.shortcuts import get_object_or_404
from django.http.response import HttpResponse
from .models import Storage
from django.conf import settings
from django.contrib.auth.decorators import login_required


@login_required()
def download_view(request, name):
    output = get_object_or_404(Storage, name__exact=name)
    path = settings.MEDIA_ROOT + output.address
    file = open(path, 'rb')
    response = HttpResponse(file, content_type='application/vnd.ms-excel')
    response['Content-Disposition'] = "attachment; filename={}".format(output.name)
    return response
