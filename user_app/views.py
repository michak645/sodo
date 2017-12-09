from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
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


def user_objects_available(request):
    pracownik = Pracownik.objects.get(id=request.session['pracownik'])
    wnioski = Wniosek.objects.filter(pracownik=pracownik)
    historia = Historia.objects.filter(wniosek__in=wnioski, status=1)
    dostepne_obiekty = []
    for wniosek in historia:
        dostepne_obiekty.append(wniosek.wniosek.obiekt)
    context = {
        'pracownik': pracownik,
        'dostepne_obiekty': dostepne_obiekty,
    }
    return render(request, 'user_app/user_objects_available.html', context)


def user_objects_list(request):
    pracownik = Pracownik.objects.get(id=request.session['pracownik'])
    wnioski = Wniosek.objects.filter(pracownik=pracownik)
    historia = Historia.objects.filter(wniosek__in=wnioski, status=1)
    dostepne_obiekty = []
    obiekty = Obiekt.objects.all()
    if request.method == 'POST':
        search = request.POST['search']
        try:
            obiekty = Obiekt.objects.filter(nazwa__contains=search)
        except Obiekt.DoesNotExist:
            messages.error(request, 'Nie znaleziono obiektu')
        if obiekty:
            context = {
                'pracownik': pracownik,
                'obiekty': obiekty,
                'search_phrase': search
            }
            return render(request, 'user_app/user_objects_list.html', context)
        else:
            context = {
                'pracownik': pracownik,
                'obiekty': obiekty,
                'search_phrase': search
            }
            return render(request, 'user_app/user_objects_list.html', context)

    for wniosek in historia:
        dostepne_obiekty.append(wniosek.wniosek.obiekt)
    context = {
        'pracownik': pracownik,
        'obiekty': obiekty,
    }
    return render(request, 'user_app/user_objects_list.html', context)


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


def user_app_add_object(request, pk):
    pracownik_id = request.session['pracownik']
    pracownik = Pracownik.objects.get(id=pracownik_id)
    obiekt = Obiekt.objects.get(pk=pk)
    if request.method == 'POST':
        form = AddApplicationForm(request.POST, initial={
            'pracownik': pracownik,
            'obiekt': obiekt
        })
        if form.is_valid():
            form.save()
            messages.success(request, 'Dodano wniosek')
            return redirect('user_index')
        else:
            messages.warning(request, 'Popraw formularz')
            messages.warning(request, '{0}'.format(form.errors.as_text()))
            return HttpResponseRedirect(reverse('user_app_add_object', kwargs={'pk': pk}))
    else:
        form = AddApplicationForm(initial={
            'pracownik': pracownik,
            'obiekt': obiekt.id
        })
    context = {
        'form': form,
        'obiekt': obiekt,
        'pracownik': pracownik,
    }
    return render(request, 'user_app/user_app_add_object.html', context)


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


def user_app_detail(request, pk):
    wniosek = Wniosek.objects.get(pk=pk)
    historia = Historia.objects.filter(wniosek=pk)
    pracownik_id = request.session['pracownik']
    pracownik = Pracownik.objects.get(id=pracownik_id)
    context = {
        'wniosek': wniosek,
        'historia': historia,
        'pracownik': pracownik,
    }
    return render(request, 'user_app/user_app_detail.html', context)