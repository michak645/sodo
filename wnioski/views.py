from django.shortcuts import render
from .models import Pracownik, Wniosek, Obiekt
from .forms import PracownikForm


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

    if request.method == 'POST':
        form = PracownikForm(request.POST)
        if form.is_valid():
            form.save()
            thanks = 'dzieki {0}'.format(form.cleaned_data['imie'])
    else:
        form = PracownikForm()

    template = "wnioski/add.html"
    context = {'form': form, 'thanks': thanks}
    return render(request, template, context)
