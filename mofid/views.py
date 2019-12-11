from django.shortcuts import render
from crawler.forms import CustomForm
from django.shortcuts import redirect
from jdatetime import datetime
from crawler.models import Storage
from crawler.crawler import crawler_engine
from django.contrib import messages


def index_view(request):
    last5output = Storage.objects.all().filter(complete=True)[:5]
    progress = Storage.objects.all().filter(complete=False)[:5]
    if request.POST:
        form = CustomForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            name = "Output_{}".format(str(datetime.now()).split('.')[-2])
            path = name + '.xlsx'
            s = Storage(name=name, complete=False, address=path, starter=request.user)
            s.save()
            crawler_engine.delay(output_name=name, sites=data["sites"], users=data["users"])
            messages.success(request, "فرآیند آغاز شد")
            return redirect('index')
    else:
        form = CustomForm()
    return render(request=request,
                  template_name='index.html',
                  context={'items': last5output, 'progress': progress, 'form': form})
