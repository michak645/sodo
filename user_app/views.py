from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.views.generic import DetailView

from .models import Cart
from auth_ex.models import (
    Pracownik,
    JednOrg,
    Labi,
)
from user_app.forms import (
    WizardUprawnienia,
)
from wnioski.models import (
    Historia, Wniosek, Obiekt, PracownicyObiektyUprawnienia,
    ZatwierdzonePrzezAS,
    AdministratorObiektu,
)
from wnioski.forms import (
    WniosekFiltrowanieForm,
    ObiektyFiltrowanieForm,
    JednostkiFiltrowanieForm,
)


def authenticate(request):
    prac = request.session['pracownik']
    try:
        pracownik = Pracownik.objects.get(pk=prac)
    except Pracownik.DoesNotExist:
        pracownik = None
    if pracownik:
        try:
            Labi.objects.get(login=pracownik)
            pracownik = None
        except Labi.DoesNotExist:
            return pracownik
    return pracownik


def logout(request):
    pracownik = request.session['pracownik']
    if pracownik:
        request.session['pracownik'] = None
    return redirect('index')


def get_latest_history(wniosek_id):
    return Historia.objects.filter(wniosek=wniosek_id).order_by('-data')[0]


def user_index(request):
    pracownik = authenticate(request)
    if not pracownik:
        messages.warning(
            request,
            'Musisz się najpierw zalogować jako pracownik'
        )
        return redirect('index')

    wnioski = Wniosek.objects.filter(pracownik=pracownik)
    historia = []
    for wniosek in wnioski:
        if get_latest_history(wniosek.id).status == '1':
            historia.append(get_latest_history(wniosek.id))

    paginator = Paginator(historia, 10)
    page = request.GET.get('page')
    try:
        historia = paginator.page(page)
    except PageNotAnInteger:
        historia = paginator.page(1)
    except EmptyPage:
        historia = paginator.page(paginator.num_pages)
    context = {
        'pracownik': pracownik,
        'historia': historia,
    }
    return render(request, 'user_app/user_index.html', context)


def user_objects_available(request):
    pracownik = authenticate(request)
    if not pracownik:
        messages.warning(
            request,
            'Musisz się najpierw zalogować jako pracownik'
        )
        return redirect('index')

    pou = PracownicyObiektyUprawnienia.objects.filter(
        login=pracownik,
    )
    obiekty_filter = pou.values('id_obiektu')
    obiekty = Obiekt.objects.filter(id__in=obiekty_filter)

    if request.method == 'POST':
        nazwa_filter = request.POST.get('nazwa_filter')
        if nazwa_filter:
            obiekty = obiekty.filter(nazwa__icontains=nazwa_filter)
    else:
        nazwa_filter = ''

    paginator = Paginator(obiekty, 10)
    page = request.GET.get('page')
    try:
        obiekty = paginator.page(page)
    except PageNotAnInteger:
        obiekty = paginator.page(1)
    except EmptyPage:
        obiekty = paginator.page(paginator.num_pages)

    context = {
        'pracownik': pracownik,
        'pou': pou,
        'obiekty': obiekty,
        'nazwa_filter': nazwa_filter,
    }
    return render(request, 'user_app/user_objects_available.html', context)


def obiekt_list(request):
    pracownik = authenticate(request)
    if not pracownik:
        messages.warning(
            request,
            'Musisz się najpierw zalogować jako pracownik'
        )
        return redirect('index')

    obiekty = Obiekt.objects.all().order_by('nazwa')
    paginacja = True
    if request.method == 'POST':
        form = ObiektyFiltrowanieForm(request.POST)
        if form.is_valid():
            if request.POST.get('clear'):
                form = ObiektyFiltrowanieForm()
            else:
                if form.cleaned_data['nazwa']:
                    obiekty = obiekty.filter(
                        nazwa__icontains=form.cleaned_data['nazwa']
                    )
                if form.cleaned_data['jednostka']:
                    jedn = form.cleaned_data['jednostka']
                    obiekty = obiekty.filter(
                        jedn_org__nazwa__icontains=jedn
                    )
                if form.cleaned_data['typ']:
                    obiekty = obiekty.filter(
                        typ__nazwa__icontains=form.cleaned_data['typ'],
                    )
                paginacja = False
    else:
        form = ObiektyFiltrowanieForm()

    paginator = Paginator(obiekty, 10)
    page = request.GET.get('page')
    try:
        obiekty = paginator.page(page)
    except PageNotAnInteger:
        obiekty = paginator.page(1)
    except EmptyPage:
        obiekty = paginator.page(paginator.num_pages)

    context = {
        'pracownik': pracownik,
        'obiekty': obiekty,
        'form': form,
        'paginacja': paginacja,
    }
    return render(request, 'user_app/user_objects_list.html', context)


class ObiektDetailView(DetailView):
    model = Obiekt
    template_name = 'user_app/obiekt_detail.html'
    context_object_name = 'obiekt'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pracownik = authenticate(self.request)
        context['pracownik'] = pracownik
        return context

    def get(self, *args, **kwargs):
        pracownik = authenticate(self.request)
        if not pracownik:
            messages.warning(
                self.request,
                'Musisz się najpierw zalogować jako pracownik'
            )
            return redirect('index')
        return super().get(*args, **kwargs)


def jednostka_list(request):
    pracownik = authenticate(request)
    if not pracownik:
        messages.warning(
            request,
            'Musisz się najpierw zalogować jako pracownik'
        )
        return redirect('index')
    jednostki = JednOrg.objects.all().order_by('nazwa')
    paginacja = True
    if request.method == 'POST':
        form = JednostkiFiltrowanieForm(request.POST)
        if form.is_valid():
            if request.POST.get('clear'):
                form = JednostkiFiltrowanieForm()
            else:
                nazwa = form.cleaned_data['nazwa']
                if nazwa:
                    jednostki = jednostki.filter(
                        nazwa__icontains=nazwa
                    )
                czy_labi = form.cleaned_data['czy_labi']
                if czy_labi:
                    jednostki = jednostki.filter(
                        czy_labi=czy_labi
                    )
                parent = form.cleaned_data['parent']
                if parent:
                    jednostki = jednostki.filter(
                        parent__nazwa__icontains=parent,
                    )
                paginacja = False
    else:
        form = JednostkiFiltrowanieForm()

    if paginacja:
        paginator = Paginator(jednostki, 10)
        page = request.GET.get('page')
        try:
            jednostki = paginator.page(page)
        except PageNotAnInteger:
            jednostki = paginator.page(1)
        except EmptyPage:
            jednostki = paginator.page(paginator.num_pages)

    context = {
        'pracownik': pracownik,
        'jednostki': jednostki,
        'form': form,
        'paginacja': paginacja,
    }
    return render(request, 'user_app/jednostka_list.html', context)


class JednostkaDetailView(DetailView):
    model = JednOrg
    template_name = 'user_app/jednostka_detail.html'
    context_object_name = 'jednostka'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        pracownik = authenticate(self.request)
        context['pracownik'] = pracownik
        if self.object.czy_labi:
            labi = Labi.objects.get(jednostka=self.object.id)
        else:
            labi = None
        context['labi'] = labi
        return context

    def get(self, *args, **kwargs):
        pracownik = authenticate(self.request)
        if not pracownik:
            messages.warning(
                self.request,
                'Musisz się najpierw zalogować jako pracownik'
            )
            return redirect('index')
        return super().get(*args, **kwargs)


def user_app_accepted(request):
    pracownik = authenticate(request)
    if not pracownik:
        messages.warning(
            request,
            'Musisz się najpierw zalogować jako pracownik'
        )
        return redirect('index')
    wnioski = Wniosek.objects.filter(pracownik=pracownik).order_by('-data')
    paginacja = True

    wnioski_przyjete = []
    for wniosek in wnioski:
        historia = Historia.objects.filter(
            wniosek=wniosek.pk).order_by('-data')[0]
        if historia.status == '3' or historia.status == '4':
            wnioski_przyjete.append(historia.wniosek.pk)

    wnioski = wnioski.filter(
        pk__in=wnioski_przyjete
    )

    if request.method == 'POST':
        form = WniosekFiltrowanieForm(request.POST)
        if form.is_valid():
            if request.POST.get('clear'):
                form = WniosekFiltrowanieForm()
            else:
                obiekt = form.cleaned_data['obiekt']
                if obiekt:
                    wnioski = wnioski.filter(
                        obiekty__nazwa__icontains=obiekt
                    )
                jednostka = form.cleaned_data['jednostka']
                if jednostka:
                    wnioski = wnioski.filter(
                        obiekty__jedn_org__nazwa__icontains=jednostka
                    )
                uprawnienia = form.cleaned_data['uprawnienia']
                if uprawnienia:
                    wnioski = wnioski.filter(
                        uprawnienia__icontains=uprawnienia,
                    )
                if form.cleaned_data['data']:
                    wnioski = wnioski.filter(
                        data__date=form.cleaned_data['data'],
                    )
                paginacja = False
    else:
        form = WniosekFiltrowanieForm()

    if paginacja:
        paginator = Paginator(wnioski, 10)
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
        'paginacja': paginacja,
        'form': form,
    }
    return render(request, 'user_app/user_app_accepted.html', context)


def user_app_rejected(request):
    pracownik = authenticate(request)
    if not pracownik:
        messages.warning(
            request,
            'Musisz się najpierw zalogować jako pracownik'
        )
        return redirect('index')
    wnioski = Wniosek.objects.filter(pracownik=pracownik).order_by('-data')
    paginacja = True
    if request.method == 'POST':
        form = WniosekFiltrowanieForm(request.POST)
        if form.is_valid():
            if request.POST.get('clear'):
                form = WniosekFiltrowanieForm()
            else:
                obiekt = form.cleaned_data['obiekt']
                if obiekt:
                    wnioski = wnioski.filter(
                        obiekty__nazwa__icontains=obiekt
                    )
                jednostka = form.cleaned_data['jednostka']
                if jednostka:
                    wnioski = wnioski.filter(
                        obiekty__jedn_org__nazwa__icontains=jednostka
                    )
                uprawnienia = form.cleaned_data['uprawnienia']
                if uprawnienia:
                    wnioski = wnioski.filter(
                        uprawnienia__icontains=uprawnienia,
                    )
                if form.cleaned_data['data']:
                    wnioski = wnioski.filter(
                        data__date=form.cleaned_data['data'],
                    )
                paginacja = False
    else:
        form = WniosekFiltrowanieForm()

    historie = []
    for wniosek in wnioski:
        historia = Historia.objects.filter(
            wniosek=wniosek.pk).order_by('-data')[0]
        if historia.status == '5':
            historie.append(historia)

    if paginacja:
        paginator = Paginator(historie, 10)
        page = request.GET.get('page')
        try:
            historie = paginator.page(page)
        except PageNotAnInteger:
            historie = paginator.page(1)
        except EmptyPage:
            historie = paginator.page(paginator.num_pages)

    context = {
        'pracownik': pracownik,
        'historie': historie,
        'paginacja': paginacja,
        'form': form,
    }
    return render(request, 'user_app/user_app_rejected.html', context)


def user_profile(request):
    pracownik = authenticate(request)
    if not pracownik:
        messages.warning(
            request,
            'Musisz się najpierw zalogować jako pracownik'
        )
        return redirect('index')
    context = {
        'pracownik': pracownik,
    }
    return render(request, 'user_app/user_profile.html', context)


def user_app_detail(request, pk):
    pracownik = authenticate(request)
    if not pracownik:
        messages.warning(
            request,
            'Musisz się najpierw zalogować jako pracownik'
        )
        return redirect('index')
    wniosek = Wniosek.objects.get(pk=pk)
    historia = Historia.objects.filter(wniosek=pk).order_by('-data')
    context = {
        'wniosek': wniosek,
        'historia': historia,
        'pracownik': pracownik,
    }
    return render(request, 'user_app/user_app_detail.html', context)


# WIZARD

def step_one(request):
    pracownik = authenticate(request)
    if not pracownik:
        messages.warning(
            request,
            'Musisz się najpierw zalogować jako pracownik'
        )
        return redirect('index')
    cart, created = Cart.objects.get_or_create(id=pracownik.pk)
    obj_list = None
    jednostka = None
    jednostki = JednOrg.objects.all().order_by('nazwa')
    wszedzie = False

    if request.method == 'POST':
        obj = request.POST.get('obj')

        szukaj_jednostki = request.POST.get('szukaj-jednostki')
        if szukaj_jednostki:
            jednostki = JednOrg.objects.filter(
                nazwa__icontains=szukaj_jednostki
            )
        szukaj_obiektu = request.POST.get('szukaj-obiektu')
        if szukaj_obiektu:
            jednostka = request.POST.get('wybrana-jednostka')
            if request.POST.get('szukaj_wszedzie'):
                obj_list = Obiekt.objects.filter(
                    nazwa__icontains=szukaj_obiektu,
                    czy_aktywny=True
                )
                wszedzie = True
            else:
                if jednostka:
                    jednostka = JednOrg.objects.get(id=jednostka)
                else:
                    messages.warning(request, 'Najpierw wybierz jednostkę')
                obj_list = Obiekt.objects.filter(
                    jedn_org=jednostka,
                    nazwa__icontains=szukaj_obiektu,
                    czy_aktywny=True
                )
                wszedzie = False

        if request.POST.get('clear'):
            cart.obiekty.clear()

        if request.POST.get('delete'):
            cart.obiekty.remove(Obiekt.objects.get(id=obj))

        if request.POST.get('add'):
            cart.obiekty.add(Obiekt.objects.get(id=obj))
            jednostka = request.POST.get('jednostka')
            if jednostka:
                obj_list = Obiekt.objects.filter(
                    jedn_org=jednostka,
                    czy_aktywny=True
                )
                jednostka = JednOrg.objects.get(id=jednostka)

        if request.POST.get('show'):
            jednostka = request.POST.get('jednostka')
            obj_list = Obiekt.objects.filter(
                jedn_org=jednostka,
                czy_aktywny=True
            )
            jednostka = JednOrg.objects.get(id=jednostka)

        if request.POST.get('dodaj_wszystkie'):
            jednostka = request.POST.get('wybrana-jednostka')
            if jednostka:
                obj_list = Obiekt.objects.filter(
                    jedn_org=jednostka,
                    czy_aktywny=True
                )
                obiekty = Obiekt.objects.filter(
                    jedn_org=jednostka,
                    czy_aktywny=True
                )
                for obiekt in obiekty:
                    cart.obiekty.add(obiekt)
                obj_list = Obiekt.objects.filter(
                    jedn_org=jednostka,
                    czy_aktywny=True
                )
        if obj_list:
            paginator = Paginator(obj_list, 10)
            page = request.GET.get('page_obiekt')
            try:
                obj_list = paginator.page(page)
            except PageNotAnInteger:
                obj_list = paginator.page(1)
            except EmptyPage:
                obj_list = paginator.page(paginator.num_pages)

    paginator = Paginator(jednostki, 10)
    page = request.GET.get('page')
    try:
        jednostki = paginator.page(page)
    except PageNotAnInteger:
        jednostki = paginator.page(1)
    except EmptyPage:
        jednostki = paginator.page(paginator.num_pages)

    objs_cart = cart.obiekty.all()
    paginator = Paginator(objs_cart, 10)
    page = request.GET.get('page')
    try:
        objs_cart = paginator.page(page)
    except PageNotAnInteger:
        objs_cart = paginator.page(1)
    except EmptyPage:
        objs_cart = paginator.page(paginator.num_pages)

    context = {
        'wybrana_jednostka': jednostka,
        'jednostki': jednostki,
        'obj_list': obj_list,
        'pracownik': pracownik,
        'objs_cart': objs_cart,
        'wszedzie': wszedzie,
    }
    return render(request, 'user_app/wizard/step_one.html', context)


def step_two(request):
    pracownik = authenticate(request)
    if not pracownik:
        messages.warning(
            request,
            'Musisz się najpierw zalogować jako pracownik'
        )
        return redirect('index')
    cart = Cart.objects.get(id=pracownik.pk)
    prac_list = None
    jednostka = None
    jednostki = JednOrg.objects.all().order_by('nazwa')
    wszedzie = False

    if request.method == 'POST':
        prac = request.POST.get('prac')

        szukaj_jednostki = request.POST.get('szukaj-jednostki')
        if szukaj_jednostki:
            jednostki = JednOrg.objects.filter(
                nazwa__icontains=szukaj_jednostki
            )

        szukaj_pracownika = request.POST.get('szukaj-pracownika')
        if szukaj_pracownika:
            jednostka = request.POST.get('wybrana-jednostka')
            if request.POST.get('szukaj_wszedzie'):
                prac_list = Pracownik.objects.filter(
                    nazwisko__icontains=szukaj_pracownika,
                    czy_aktywny=True
                )
                wszedzie = True
            else:
                if jednostka:
                    jednostka = JednOrg.objects.get(id=jednostka)
                else:
                    messages.warning(request, 'Najpierw wybierz jednostkę')
                prac_list = Pracownik.objects.filter(
                    jedn_org=jednostka,
                    nazwisko__icontains=szukaj_pracownika,
                    czy_aktywny=True,
                )
                wszedzie = False

        if request.POST.get('clear'):
            cart.pracownicy.clear()

        if request.POST.get('delete'):
            cart.pracownicy.remove(Pracownik.objects.get(login=prac))

        if request.POST.get('add'):
            cart.pracownicy.add(Pracownik.objects.get(login=prac))
            jednostka = request.POST.get('jednostka')
            if jednostka:
                prac_list = Pracownik.objects.filter(
                    jedn_org=jednostka,
                    czy_aktywny=True,
                )
                jednostka = JednOrg.objects.get(id=jednostka)

        if request.POST.get('show'):
            jednostka = request.POST.get('jednostka')
            prac_list = Pracownik.objects.filter(
                jedn_org=jednostka,
                czy_aktywny=True,
            )
            jednostka = JednOrg.objects.get(id=jednostka)

        if request.POST.get('dodaj_wszystkie'):
            jednostka = request.POST.get('wybrana-jednostka')
            if jednostka:
                prac_list = Pracownik.objects.filter(
                    jedn_org=jednostka,
                    czy_aktywny=True
                )
                pracownicy_temp = Pracownik.objects.filter(
                    jedn_org=jednostka,
                    czy_aktywny=True
                )
                for pracownik in pracownicy_temp:
                    cart.pracownicy.add(pracownik)
                prac_list = Pracownik.objects.filter(
                    jedn_org=jednostka,
                    czy_aktywny=True
                )

        if prac_list:
            paginator = Paginator(prac_list, 10)
            page = request.GET.get('page_obiekt')
            try:
                prac_list = paginator.page(page)
            except PageNotAnInteger:
                prac_list = paginator.page(1)
            except EmptyPage:
                prac_list = paginator.page(paginator.num_pages)

    paginator = Paginator(jednostki, 10)
    page = request.GET.get('page')
    try:
        jednostki = paginator.page(page)
    except PageNotAnInteger:
        jednostki = paginator.page(1)
    except EmptyPage:
        jednostki = paginator.page(paginator.num_pages)

    prac_cart = cart.pracownicy.all()
    paginator = Paginator(prac_cart, 10)
    page = request.GET.get('page')
    try:
        prac_cart = paginator.page(page)
    except PageNotAnInteger:
        prac_cart = paginator.page(1)
    except EmptyPage:
        prac_cart = paginator.page(paginator.num_pages)

    context = {
        'wybrana_jednostka': jednostka,
        'jednostki': jednostki,
        'pracownik': pracownik,
        'prac_list': prac_list,
        'prac_cart': prac_cart,
        'wszedzie': wszedzie,
    }
    return render(request, 'user_app/wizard/step_two.html', context)


def step_three(request):
    pracownik = authenticate(request)
    if not pracownik:
        messages.warning(
            request,
            'Musisz się najpierw zalogować jako pracownik'
        )
        return redirect('index')
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
        obiekty[obiekt] = pracownicy

    if request.method == 'POST':
        form = WizardUprawnienia(request.POST)
        if form.is_valid():
            cart.uprawnienia = form.cleaned_data['uprawnienia']
            cart.typ_wniosku = form.cleaned_data['typ_wniosku']
            cart.save()
            return redirect('step_four')
        else:
            messages.error(request, 'Wypełnij poprawnie formularz')
    else:
        form = WizardUprawnienia()

    pracownicy = cart.pracownicy.all()

    paginator = Paginator(pracownicy, 10)
    page = request.GET.get('page')
    try:
        pracownicy = paginator.page(page)
    except PageNotAnInteger:
        pracownicy = paginator.page(1)
    except EmptyPage:
        pracownicy = paginator.page(paginator.num_pages)

    context = {
        'pracownik': pracownik,
        'pracownicy': pracownicy,
        'cart': cart,
        'aktualne_uprawnienia': aktualne_uprawnienia,
        'form': form,
        'obiekty': obiekty,
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
    pracownik = authenticate(request)
    if not pracownik:
        messages.warning(
            request,
            'Musisz się najpierw zalogować jako pracownik'
        )
        return redirect('index')
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
        wniosek['uprawnienia'] = cart.get_uprawnienia_display()
        wniosek['typ_wniosku'] = cart.get_typ_wniosku_display()
        wnioski.append(wniosek)

    if request.method == 'POST':
        for wniosek in wnioski:
            w = Wniosek.objects.create(
                typ=cart.typ_wniosku,
                pracownik=pracownik,
                uprawnienia=cart.uprawnienia,
            )
            for prac_temp in cart.pracownicy.all():
                w.pracownicy.add(prac_temp)
            for obiekt in wniosek['obiekty']:
                w.obiekty.add(obiekt)
            komentarz_id = 'komentarz' + str(wniosek['labi'].id)
            komentarz = request.POST.get(komentarz_id)
            w.komentarz = komentarz
            w.save()
            ''' zakomentowane bo dlugo robi i nie chce spamowac, zreszta maile pracownikow sa fejkowe
            subject = 'SODO: nowy wniosek nr '+str(w.pk)+' w systemie'
            message = 'Złożyłeś nowy wniosek w systemie SODO.\nWniosek otrzymał numer '+str(w.pk)+', ' \
                'został umieszczony w systemie i oczekuje na decyzję Lokalnego Administratora ' \
                'Bezpieczeństwa Informacji.\nDokument w formacie PDF został dołączony do tej wiadomości.\n' \
                'Wiadomość wygenerowana automatycznie.'
            send_addr = w.pracownik.email
            email = EmailMessage(subject, message, 'sodo.uam.test@gmail.com', [send_addr])
            html = render_to_string('PDF_wnioski/wniosek_pdf_wzor.html', {'wniosek': w, 'pracownik': pracownik})
            out = BytesIO()
            weasyprint.HTML(string=html).write_pdf(out)
            email.attach('wniosek'+str(w.pk)+'.pdf', out.getvalue(), 'application/pdf')
            email.send()
            '''
        cart.delete()
        return HttpResponseRedirect('/user_index')
    context = {
        'wnioski': wnioski,
        'pracownik': pracownik,
        'cart': cart,
    }
    return render(request, 'user_app/wizard/step_four.html', context)


def admin_panel(request):
    pracownik = authenticate(request)
    if not pracownik:
        messages.warning(
            request,
            'Musisz się najpierw zalogować jako pracownik'
        )
        return redirect('index')

    obiekty_admina = AdministratorObiektu.objects.filter(pracownik=pracownik)

    if request.method == 'POST':
        lista = request.POST.getlist('zatwierdzone')
        for elem in lista:
            obj = ZatwierdzonePrzezAS.objects.get(id=elem)
            obj.zatwierdzone = True
            obj.save()
            Historia.objects.create(
                wniosek=obj.wniosek,
                status='4',
                pracownik=pracownik,
            )

    to_approve = []
    for obiekt in obiekty_admina:
        lista_elem = ZatwierdzonePrzezAS.objects.filter(
            obiekt=obiekt.obiekt,
            zatwierdzone=False,
        )
        if lista_elem:
            for elem in lista_elem:
                to_approve.append(elem)

    context = {
        'pracownik': pracownik,
        'wnioski': to_approve,
    }
    return render(request, 'user_app/admin_panel.html', context)


def admin_panel_detail(request, pk):
    pracownik = authenticate(request)
    if not pracownik:
        messages.warning(
            request,
            'Musisz się najpierw zalogować jako pracownik'
        )
        return redirect('index')

    obiekt = ZatwierdzonePrzezAS.objects.get(pk=pk)

    context = {
        'pracownik': pracownik,
        'obiekt': obiekt,
    }
    return render(request, 'user_app/admin_panel_default.html', context)
