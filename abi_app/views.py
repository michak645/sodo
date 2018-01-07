from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib import messages

from auth_ex.models import Labi, Pracownik, JednOrg
from user_app.forms import WizardUprawnienia
from user_app.models import Cart
from wnioski.models import (
    Wniosek,
    Historia,
    PracownicyObiektyUprawnienia,
    Obiekt,
    ZatwierdzonePrzezAS,
)


def abi_index(request):
    pracownik = Labi.objects.get(id=request.session['pracownik'])

    if request.method == 'POST':
        wnioski = Wniosek.objects.all().order_by('data')
        data_nowe = request.POST.get('data-nowe')
        data_stare = request.POST.get('data-stare')
        if data_nowe:
            wnioski = Wniosek.objects.order_by('-data')
        elif data_stare:
            wnioski = Wniosek.objects.order_by('data')

        if request.POST.get('zatwierdz'):
            checked = request.POST.getlist('decyzja')

            for pk in checked:
                w = Wniosek.objects.get(id=pk)
                Historia.objects.create(
                    wniosek_id=pk,
                    status='3',
                )
                if w.typ == '1':
                    for obiekt in w.obiekty.all():
                        for pracownik in w.pracownicy.all():
                            for uprawnienia in w.uprawnienia:
                                PracownicyObiektyUprawnienia.objects \
                                    .get_or_create(
                                        login=pracownik,
                                        id_obiektu=obiekt,
                                        uprawnienia=uprawnienia
                                    )
                        ZatwierdzonePrzezAS.objects.create(
                            wniosek=w,
                            obiekt=obiekt,
                        )
                elif w.typ == '2':
                    try:
                        for obiekt in w.obiekty.all():
                            for pracownik in w.pracownicy.all():
                                for uprawnienia in w.uprawnienia:
                                    PracownicyObiektyUprawnienia.objects.get(
                                        login=pracownik,
                                        id_obiektu=obiekt,
                                        uprawnienia=uprawnienia
                                    ).delete()
                            ZatwierdzonePrzezAS.objects.create(
                                wniosek=w,
                                obiekt=obiekt,
                            )
                    except PracownicyObiektyUprawnienia.DoesNotExist:
                        pass
        elif request.POST.get('odrzuc'):
            Historia.objects.create(
                wniosek_id=pk,
                status='5',
            )
            historia = Historia.objects.filter(wniosek=pk)
            return HttpResponseRedirect('/abi_index')
    else:
        wnioski = Wniosek.objects.all().order_by('data')

    to_approve = []
    for wniosek in wnioski:
        historia = Historia.objects.filter(
            wniosek=wniosek.id,
        ).order_by('-data')[0]
        if historia.status == '2':
            to_approve.append(historia)

    context = {
        'wnioski': to_approve,
        'pracownik': pracownik,
    }
    return render(request, 'abi_app/abi_index.html', context)


def wniosek_list(request):
    pracownik = Labi.objects.get(id=request.session['pracownik'])

    if request.method == 'POST':
        search = request.POST.get('search')
        if search:
            wnioski_list = Wniosek.objects.filter(
                pracownik__nazwisko__icontains=search,
            ).order_by('-data')
        else:
            wnioski_list = Wniosek.objects.all().order_by('-data')
    else:
        wnioski_list = Wniosek.objects.all().order_by('-data')

    paginator = Paginator(wnioski_list, 20)

    page = request.GET.get('page')
    try:
        wnioski = paginator.page(page)
    except PageNotAnInteger:
        wnioski = paginator.page(1)
    except EmptyPage:
        wnioski = paginator.page(paginator.num_pages)

    context = {
        'pracownik': pracownik,
        'wnioski': wnioski,
    }
    return render(request, 'abi_app/wniosek_list.html', context)


def wniosek_detail(request, pk):
    w = Wniosek.objects.get(id=pk)
    if request.method == 'POST':
        if request.POST.get('change') == "Zatwierdź":
            Historia.objects.create(
                wniosek_id=pk,
                status='3',
            )
            historia = Historia.objects. \
                filter(wniosek=pk). \
                order_by('-data')
        elif request.POST.get('change') == "Odrzuć":
            Historia.objects.create(
                wniosek_id=pk,
                status='5',
            )
            historia = Historia.objects.filter(wniosek=pk)
    else:
        historia = Historia.objects. \
            filter(wniosek=pk). \
            order_by('-data')
    context = {
        'wniosek': w,
        'historia': historia,
        'status': historia[0].get_status_display(),
        'status_id': historia[0].status,
    }
    return render(request, 'abi_app/wniosek_detail.html', context)


def obiekt_list(request):
    obiekty = Obiekt.objects.all()
    if request.method == 'POST':
        search = request.POST['search']
        try:
            obiekty = Obiekt.objects.filter(nazwa__contains=search)
        except Obiekt.DoesNotExist:
            messages.error(request, 'Nie znaleziono obiektu')
        if obiekty:
            context = {
                'obiekty': obiekty,
                'search_phrase': search
            }
            return render(request, 'abi_app/data/obiekt_list.html', context)
        else:
            context = {
                'obiekty': obiekty,
                'search_phrase': search
            }
            return render(request, 'abi_app/data/obiekt_list.html', context)

    context = {
        'obiekty': obiekty,
    }
    return render(request, 'abi_app/data/obiekt_list.html', context)


def obiekt_detail(request):
    return render(request, 'abi_app/obiekt_list.html')


# WIZARD
def step_one(request):
    labi = Labi.objects.get(id=request.session['pracownik'])
    pracownik = Pracownik.objects.get(pk=labi.login.pk)
    cart, created = Cart.objects.get_or_create(id=pracownik.pk)
    obj_list = None
    jednostka = None
    jednostki = JednOrg.objects.all()

    paginator = Paginator(jednostki, 10)
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
    return render(request, 'abi_app/wizard/step_one.html', context)


def step_two(request):
    labi = Labi.objects.get(id=request.session['pracownik'])
    pracownik = Pracownik.objects.get(pk=labi.login.pk)
    cart = Cart.objects.get(id=pracownik.pk)
    prac_list = None
    jednostka = None
    jednostki = JednOrg.objects.all()

    paginator = Paginator(jednostki, 10)
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
    return render(request, 'abi_app/wizard/step_two.html', context)


def step_three(request):
    labi = Labi.objects.get(id=request.session['pracownik'])
    pracownik = Pracownik.objects.get(pk=labi.login.pk)
    cart = Cart.objects.get(id=pracownik.pk)
    aktualne_uprawnienia = PracownicyObiektyUprawnienia.objects.filter(
        login__in=cart.pracownicy.all(),
        id_obiektu__in=cart.obiekty.all()
    )

    obiekty = {}
    for obiekt in cart.obiekty.all():
        pracownicy = {}
        for pracownik in cart.pracownicy.all():
            pou = PracownicyObiektyUprawnienia.objects.filter(
                login=pracownik,
                id_obiektu=obiekt,
            )
            if pou:
                pracownicy[pracownik] = pou
        print(pracownicy)
        obiekty[obiekt] = pracownicy

    if request.method == 'POST':
        form = WizardUprawnienia(request.POST)
        if form.is_valid():
            cart.uprawnienia = form.cleaned_data['uprawnienia']
            cart.typ_wniosku = form.cleaned_data['typ_wniosku']
            cart.save()
            return redirect('step_four')
    else:
        form = WizardUprawnienia()
    context = {
        'pracownik': pracownik,
        'cart': cart,
        'aktualne_uprawnienia': aktualne_uprawnienia,
        'form': form,
        'obiekty': obiekty,
    }
    return render(request, 'abi_app/wizard/step_three.html', context)


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
    labi = Labi.objects.get(id=request.session['pracownik'])
    pracownik = Pracownik.objects.get(pk=labi.login.pk)
    cart = Cart.objects.get(id=pracownik.pk)

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
        return HttpResponseRedirect('/abi_index')
    context = {
        'wnioski': wnioski,
        'pracownik': pracownik,
        'cart': cart,
    }
    return render(request, 'abi_app/wizard/step_four.html', context)
