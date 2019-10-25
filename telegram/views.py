from django.shortcuts import render
# from .task import generate_report
from django.http.response import HttpResponse
from .telegram import send_message
# from django.views.generic import TemplateView
from crawler.models import Storage


def my_view(request):
    send_message(65908245, 'test1')
    #    generate_report.delay(65908245, "OK. It's work.")
    return HttpResponse("You will receive an telegram message when the report is done")


def index_view(requests):
    last5output = Storage.objects.all()[:5]


    return render(requests, template_name='index.html', context=context)
