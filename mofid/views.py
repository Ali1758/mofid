from django.shortcuts import render
from crawler.models import Storage
from crawler.forms import CustomForm
from django.shortcuts import redirect
from datetime import datetime
from crawler.models import Storage
from crawler.crawler import crawler_engine
from django.contrib import messages


def index_view(request):
    last5output = Storage.objects.all().filter(complete=True)[:5]
    if request.POST:
        form = CustomForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            name = "Output_{}".format(str(datetime.now()).split('.')[-2])
            path = name + '.xlsx'
            s = Storage(name=name, complete=False, address=path, starter=request.user, type='All')
            s.save()
            crawler_engine.delay(outputname=name, sites=data.sites, users=data["users"])
            messages.success(request, "فرآیند آغاز شد")
            return redirect('index')
    else:
        form = CustomForm()
    return render(request, template_name='index.html', context={'items': last5output, 'form': form})
