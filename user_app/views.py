from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse

from .models import Cart
from auth_ex.models import (
    Pracownik,
    JednOrg,
    Labi,
)
from user_app.forms import (
    AddApplicationForm,
    WizardUprawnienia
)
from wnioski.models import (
    Historia, Wniosek, Obiekt, PracownicyObiektyUprawnienia
)


def get_latest_history(wniosek_id):
    return Historia.objects.filter(wniosek=wniosek_id).order_by('-data')[0]


def user_index(request):
    pracownik = Pracownik.objects.get(login=request.session['pracownik'])
    wnioski = Wniosek.objects.filter(pracownik=pracownik)
    historia = []
    for wniosek in wnioski:
        if get_latest_history(wniosek.id).status == '3':
            historia.append(get_latest_history(wniosek.id))
    context = {
        'pracownik': pracownik,
        'historia': historia,
    }
    return render(request, 'user_app/user_index.html', context)


def user_objects_available(request):
    pracownik = Pracownik.objects.get(login=request.session['pracownik'])
    obiekty = PracownicyObiektyUprawnienia.objects.filter(
        login=pracownik
    )
    context = {
        'pracownik': pracownik,
        'dostepne_obiekty': obiekty,
    }
    return render(request, 'user_app/user_objects_available.html', context)


def user_objects_list(request):
    pracownik = Pracownik.objects.get(login=request.session['pracownik'])
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
        dostepne_obiekty.append(wniosek.wniosek.obiekty)
    context = {
        'pracownik': pracownik,
        'obiekty': obiekty,
    }
    return render(request, 'user_app/user_objects_list.html', context)


def user_add_app(request):
    pracownik_id = request.session['pracownik']
    pracownik = Pracownik.objects.get(login=pracownik_id)
    if request.method == 'POST':
        form = AddApplicationForm(request.POST, initial={
            'pracownik': pracownik})
        if form.is_valid():
            try:
                query = Wniosek.objects.filter(
                    pracownik=form.cleaned_data['pracownik'],
                    typ=form.cleaned_data['typ'],
                    uprawnienia=form.cleaned_data['uprawnienia'],
                    obiekt=form.cleaned_data['obiekt']
                ).order_by('-data')[0]
            except IndexError:
                query = None

            if query:
                wnioski = Wniosek.objects.filter(
                    pracownik=form.cleaned_data['pracownik'],
                    obiekt=form.cleaned_data['obiekt'],
                    uprawnienia=form.cleaned_data['uprawnienia']
                )
                historia = Historia.objects.filter(
                    wniosek__in=wnioski
                ).order_by('-data')[0]
                '''
                status zatwierdzony/przetwarzanie/odrzucony
                dla przetwarzanego odrzucamy zawsze
                '''
                if historia.status == '3':
                    messages.warning(
                        request,
                        'Wniosek do obiektu {0} o uprawnieniu {1}'
                        ' jest przetwarzany'.
                        format(
                            historia.wniosek.obiekt,
                            historia.wniosek.get_uprawnienia_display()
                        )
                    )
                    return redirect('user_index')

                '''
                typ wniosku, przyznanie uprawnien lub odrzucenie
                jeśli przyznano uprawnienia, to zezwalamy tylko na
                odrzucanie i na odwrót
                '''
                if historia.wniosek.typ == form.cleaned_data['typ'] \
                   and historia.status == '1':
                    messages.warning(
                        request,
                        'Taki wniosek został już złożony i zatwierdzony'
                    )
                    return redirect('user_index')

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
    pracownik = Pracownik.objects.get(login=pracownik_id)
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
            return HttpResponseRedirect(
                reverse('user_app_add_object', kwargs={'pk': pk}))
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
    pracownik = Pracownik.objects.get(login=pracownik_id)
    wnioski = Wniosek.objects.filter(pracownik=pracownik_id)
    historie = []
    for wniosek in wnioski:
        historia = Historia.objects.filter(
            wniosek=wniosek.pk).order_by('-data')[0]
        if historia.status == '1':
            historie.append(historia)
    context = {
        'pracownik': pracownik,
        'historie': historie,
    }
    return render(request, 'user_app/user_app_accepted.html', context)


def user_app_rejected(request):
    pracownik_id = request.session['pracownik']
    pracownik = Pracownik.objects.get(login=pracownik_id)
    wnioski = Wniosek.objects.filter(pracownik=pracownik_id)
    historie = []
    for wniosek in wnioski:
        historia = Historia.objects.filter(
            wniosek=wniosek.pk).order_by('-data')[0]
        if historia.status == '2':
            historie.append(historia)
    context = {
        'pracownik': pracownik,
        'historie': historie,
    }
    return render(request, 'user_app/user_app_rejected.html', context)


def user_profile(request):
    pracownik_id = request.session['pracownik']
    pracownik = Pracownik.objects.get(login=pracownik_id)
    context = {
        'pracownik': pracownik,
    }
    return render(request, 'user_app/user_profile.html', context)


def user_app_detail(request, pk):
    wniosek = Wniosek.objects.get(pk=pk)
    historia = Historia.objects.filter(wniosek=pk).order_by('-data')
    pracownik_id = request.session['pracownik']
    pracownik = Pracownik.objects.get(login=pracownik_id)
    context = {
        'wniosek': wniosek,
        'historia': historia,
        'pracownik': pracownik,
    }
    return render(request, 'user_app/user_app_detail.html', context)


# WIZARD

def step_one(request):
    pracownik_id = request.session['pracownik']
    pracownik = Pracownik.objects.get(login=pracownik_id)
    cart, created = Cart.objects.get_or_create(id=pracownik_id)
    obj_list = None
    jednostka = None
    jednostki = JednOrg.objects.all()

    paginator = Paginator(jednostki, 4)
    page = request.GET.get('page')
    try:
        jedn = paginator.page(page)
    except PageNotAnInteger:
        jedn = paginator.page(1)
    except EmptyPage:
        jedn = paginator.page(paginator.num_pages)

    if request.method == 'POST':
        clear = request.POST.get('clear')
        if clear:
            cart.obiekty.clear()
        obj = request.POST.get('obj')
        add = request.POST.get('add')
        delete = request.POST.get('delete')
        if delete:
            cart.obiekty.remove(Obiekt.objects.get(id=obj))
        if add:
            cart.obiekty.add(Obiekt.objects.get(id=obj))
        show = request.POST.get('show')
        if show:
            jednostka = request.POST.get('jednostka')
            obj_list = Obiekt.objects.filter(jedn_org=jednostka)
            jednostka = JednOrg.objects.get(id=jednostka).nazwa

    context = {
        'wybrana_jednostka': jednostka,
        'jednostki': jedn,
        'obj_list': obj_list,
        'pracownik': pracownik,
        'objs_cart': cart.obiekty.all(),
    }
    return render(request, 'user_app/wizard/step_one.html', context)


def step_two(request):
    pracownik_id = request.session['pracownik']
    pracownik = Pracownik.objects.get(login=pracownik_id)
    cart = Cart.objects.get(id=pracownik_id)
    prac_list = None
    jednostka = None
    jednostki = JednOrg.objects.all()

    paginator = Paginator(jednostki, 4)
    page = request.GET.get('page')
    try:
        jedn = paginator.page(page)
    except PageNotAnInteger:
        jedn = paginator.page(1)
    except EmptyPage:
        jedn = paginator.page(paginator.num_pages)

    if request.method == 'POST':
        clear = request.POST.get('clear')
        if clear:
            cart.pracownicy.clear()
        prac = request.POST.get('prac')
        add_prac = request.POST.get('add_prac')
        show = request.POST.get('show')
        if show:
            jednostka = request.POST.get('jednostka')
            prac_list = Pracownik.objects.filter(jedn_org=jednostka)
            jednostka = JednOrg.objects.get(id=jednostka).nazwa
        if add_prac:
            cart.pracownicy.add(Pracownik.objects.get(login=prac))
        delete_prac = request.POST.get('delete_prac')
        if delete_prac:
            cart.pracownicy.remove(Pracownik.objects.get(login=prac))
    context = {
        'wybrana_jednostka': jednostka,
        'jednostki': jedn,
        'pracownik': pracownik,
        'prac_list': prac_list,
        'prac_cart': cart.pracownicy.all(),
    }
    return render(request, 'user_app/wizard/step_two.html', context)


def step_three(request):
    # czy_chcesz_zostac_dodany_do_wnioski_checkbox = False
    pracownik_id = request.session['pracownik']
    pracownik = Pracownik.objects.get(login=pracownik_id)
    cart = Cart.objects.get(id=pracownik_id)
    aktualne_uprawnienia = PracownicyObiektyUprawnienia.objects.filter(
        login__in=cart.pracownicy.all(),
        id_obiektu__in=cart.obiekty.all()
    )
    if request.method == 'POST':
        form = WizardUprawnienia(request.POST)
        if form.is_valid():
            cart.uprawnienia = form.cleaned_data['uprawnienia']
            cart.typ_wniosku = form.cleaned_data['typ_wniosku']
            cart.save()
            return HttpResponseRedirect('/wizard/step_four')
    else:
        form = WizardUprawnienia()
    context = {
        'pracownik': pracownik,
        'cart': cart,
        'aktualne_uprawnienia': aktualne_uprawnienia,
        'form': form
    }
    return render(request, 'user_app/wizard/step_three.html', context)


def get_labi(jedn):
    try:
        jednostka = JednOrg.objects.get(id=jedn)
    except JednOrg.DoesNotExist as e:
        return e
    if jednostka.czy_labi:
        return Labi.objects.get(jednostka=jednostka.id)
    else:
        return get_labi(jednostka.parent.id)


def step_four(request):
    pracownik_id = request.session['pracownik']
    pracownik = Pracownik.objects.get(login=pracownik_id)
    cart = Cart.objects.get(id=pracownik_id)

    cart_objs = cart.obiekty.all()
    labi_list = []
    for obj in cart_objs:
        if get_labi(obj.jedn_org.id) not in labi_list:
            labi_list.append(get_labi(obj.jedn_org.id))

    wnioski = []
    for labi in labi_list:
        wniosek = {}
        wniosek['labi'] = labi
        wniosek_obiekty = []
        for obj in cart_objs:
            if get_labi(obj.jedn_org.id) == labi:
                wniosek_obiekty.append(obj)
        wniosek['obiekty'] = wniosek_obiekty
        wniosek['pracownicy'] = cart.pracownicy.all()
        wniosek['uprawnienia'] = cart.uprawnienia
        wniosek['typ_wniosku'] = cart.typ_wniosku
        wnioski.append(wniosek)

    if request.method == 'POST':
        for wniosek in wnioski:
            w = Wniosek.objects.create(
                typ=cart.typ_wniosku,
                pracownik=pracownik,
                uprawnienia=cart.uprawnienia,
            )
            for pracownik in cart.pracownicy.all():
                w.pracownicy.add(pracownik)
            for obiekt in wniosek['obiekty']:
                w.obiekty.add(obiekt)
            w.save()
        cart.delete()
        return HttpResponseRedirect('/user_index')
    context = {
        'wnioski': wnioski,
        'pracownik': pracownik,
        'cart': cart,
    }
    return render(request, 'user_app/wizard/step_four.html', context)
