from django.shortcuts import render
from crawler.models import Storage
from crawler.forms import SelectCrawlingModelForm
from django.shortcuts import redirect


def index_view(requests):
    last5output = Storage.objects.all().filter(complete=True)[:5]
    if requests.POST:
        form = SelectCrawlingModelForm(requests.POST)
        if form.is_valid():
            option = form.cleaned_data['option']
            if option == 'custom':
                return redirect('custom_crawling')
            elif option == 'all':
                return redirect('full_crawling')
    else:
        form = SelectCrawlingModelForm()
    return render(requests, template_name='index.html', context={'items': last5output, 'form': form})
