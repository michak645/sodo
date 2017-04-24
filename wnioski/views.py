from django.shortcuts import render
from .models import Pracownik, Wniosek, Obiekt
from .forms import WniosekForm
from django.utils import formats


def index(request):

    # import pdb
    # pdb.set_trace()

    pracownik = Pracownik.objects.all()
    obiekt = Obiekt.objects.all()
    wniosek = Wniosek.objects.order_by('-data_zlo')[:5]

    template = "wnioski/index.html"
    context = {
        'pracownik': pracownik,
        'obiekt': obiekt,
        'wniosek': wniosek
    }
    return render(request, template, context)


def add(request):

    thanks = ''

# thanks = 'dzieki {0}'.format(form.cleaned_data['imie'])

    if request.method == 'POST':
        form = WniosekForm(request.POST)
        if form.is_valid():
            form.save()
            thanks = 'wniosek dodany w dniu {0}'.format(
                formats.date_format(
                    form.cleaned_data['data_zlo'],
                    "SHORT_DATETIME_FORMAT"
                )
            )
    else:
        form = WniosekForm()

    template = "wnioski/add.html"
    context = {'form': form, 'thanks': thanks}
    return render(request, template, context)
