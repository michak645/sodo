from django.shortcuts import render
from .models import Pracownik, Wniosek, Obiekt
from .forms import WniosekForm


def index(request):

    # import pdb
    # pdb.set_trace()

    pracownik = Pracownik.objects.all()
    obiekt = Obiekt.objects.all()
    wniosek = Wniosek.objects.all()

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
        formWniosek = WniosekForm(request.POST)
        if formWniosek.is_valid():
            formWniosek.save()
            thanks = 'wniosek dodany w dniu {0}'.format(
                formWniosek.cleaned_data['data_zlo']
            )
    else:
        formWniosek = WniosekForm()

    template = "wnioski/add.html"
    context = {'formWniosek': formWniosek, 'thanks': thanks}
    return render(request, template, context)
