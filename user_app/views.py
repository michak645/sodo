from django.contrib import messages
from django.shortcuts import render, redirect
from django.views.generic import DetailView

from auth_ex.models import Pracownik
from user_app.forms import AddApplicationForm
from wnioski.models import Historia, Wniosek, Obiekt


def user_index(request):
    pracownik = Pracownik.objects.get(id=request.session['pracownik'])
    wnioski = Wniosek.objects.filter(pracownik=pracownik)
    historia = Historia.objects.filter(wniosek__in=wnioski, status=3)
    context = {
        'pracownik': pracownik,
        'historia': historia,
    }
    return render(request, 'user_app/user_index.html', context)


def user_objects(request):
    pracownik = Pracownik.objects.get(id=request.session['pracownik'])
    wnioski = Wniosek.objects.filter(pracownik=pracownik)
    historia = Historia.objects.filter(wniosek__in=wnioski, status=1)
    obiekty = []
    for wniosek in historia:
        obiekty.append(wniosek.wniosek.obiekt)
    context = {
        'pracownik': pracownik,
        'obiekty': obiekty,
    }
    return render(request, 'user_app/user_objects.html', context)


def user_add_app(request):
    pracownik_id = request.session['pracownik']
    pracownik = Pracownik.objects.get(id=pracownik_id)
    if request.method == 'POST':
        form = AddApplicationForm(request.POST, initial={'pracownik': pracownik})
        if form.is_valid():
            form.save()
            messages.success(request, 'Dodano wniosek')
            return redirect('user_index')
        else:
            messages.warning(request, 'Popraw formularz')
            return redirect('user_add_app')
    else:
        form = AddApplicationForm(initial={'pracownik': pracownik})
    context = {
        'pracownik': pracownik,
        'form': form,
    }
    return render(request, 'user_app/user_add_app.html', context)


def user_app_accepted(request):
    pracownik_id = request.session['pracownik']
    pracownik = Pracownik.objects.get(id=pracownik_id)
    wnioski = Wniosek.objects.filter(pracownik=pracownik_id)
    historia = Historia.objects.filter(wniosek__in=wnioski, status=1)
    context = {
        'pracownik': pracownik,
        'historia': historia,
    }
    return render(request, 'user_app/user_app_accepted.html', context)


def user_app_rejected(request):
    pracownik_id = request.session['pracownik']
    pracownik = Pracownik.objects.get(id=pracownik_id)
    wnioski = Wniosek.objects.filter(pracownik=pracownik_id)
    historia = Historia.objects.filter(wniosek__in=wnioski, status=2)
    context = {
        'pracownik': pracownik,
        'historia': historia,
    }
    return render(request, 'user_app/user_app_rejected.html', context)


def user_profile(request):
    pracownik_id = request.session['pracownik']
    pracownik = Pracownik.objects.get(id=pracownik_id)
    context = {
        'pracownik': pracownik,
    }
    return render(request, 'user_app/user_profile.html', context)


class AppDetailView(DetailView):
    model = Wniosek
    context_object_name = 'wniosek'
    template_name = 'user_app/user_app_detail.html'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        context['historia'] = Historia.objects.filter(wniosek=self.kwargs['pk'])
        return context

