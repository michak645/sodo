from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib import messages
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

from auth_ex.models import Labi, Pracownik, JednOrg, RodzajPracownika
from user_app.forms import WizardUprawnienia
from user_app.models import Cart
from wnioski.models import *


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
    Historia, Wniosek, Obiekt, PracownicyObiektyUprawnienia,
    ZatwierdzonePrzezAS,
    AdministratorObiektu,
)


def get_latest_history(wniosek_id):
    return Historia.objects.filter(wniosek=wniosek_id).order_by('-data')[0]


def user_index(request):
    pracownik = Pracownik.objects.get(login=request.session['pracownik'])
    wnioski = Wniosek.objects.filter(pracownik=pracownik)
    historia = []
    for wniosek in wnioski:
        if get_latest_history(wniosek.id).status == '1':
            historia.append(get_latest_history(wniosek.id))
    context = {
        'pracownik': pracownik,
        'historia': historia,
    }
    return render(request, 'user_app/user_index.html', context)


def user_objects_available(request):
    pracownik = Pracownik.objects.get(login=request.session['pracownik'])

    wnioski = Wniosek.objects.all()
    wnioski_pracownika = []
    for wniosek in wnioski:
        for prac_wniosek in wniosek.pracownicy.all():
            if prac_wniosek.pk == pracownik.pk:
                wnioski_pracownika.append(wniosek)

    obiekty_zatwierdzone = ZatwierdzonePrzezAS.objects.filter(
        wniosek__in=wnioski_pracownika,
    )

    context = {
        'pracownik': pracownik,
        'obiekty': obiekty_zatwierdzone,
    }
    return render(request, 'user_app/user_objects_available.html', context)


class ObiektListView(ListView):
    model = Obiekt
    template_name = 'user_app/user_objects_list.html'
    context_object_name = 'obiekty'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        paginator = Paginator(self.get_queryset(), 10)
        page = self.request.GET.get('page')
        try:
            obiekty = paginator.page(page)
        except PageNotAnInteger:
            obiekty = paginator.page(1)
        except EmptyPage:
            obiekty = paginator.page(paginator.num_pages)
        context['obiekty'] = obiekty
        return context

    def post(self, request, *args, **kwargs):
        search = request.POST.get('search')
        if search:
            obiekty = self.get_queryset(). \
                filter(nazwa__icontains=search)
        else:
            obiekty = self.get_queryset()
        paginator = Paginator(obiekty, 10)
        page = self.request.GET.get('page')
        try:
            obiekty = paginator.page(page)
        except PageNotAnInteger:
            obiekty = paginator.page(1)
        except EmptyPage:
            obiekty = paginator.page(paginator.num_pages)
        context = {
            'obiekty': obiekty,
            'search': search,
        }
        return render(request, self.template_name, context)


class ObiektDetailView(DetailView):
    model = Obiekt
    template_name = 'user_app/obiekt_detail.html'
    context_object_name = 'obiekt'


class JednostkaListView(ListView):
    model = JednOrg
    template_name = 'user_app/jednostka_list.html'
    context_object_name = 'jednostki'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        paginator = Paginator(self.get_queryset(), 10)
        page = self.request.GET.get('page')
        try:
            jednostki = paginator.page(page)
        except PageNotAnInteger:
            jednostki = paginator.page(1)
        except EmptyPage:
            jednostki = paginator.page(paginator.num_pages)
        context['jednostki'] = jednostki
        return context

    def post(self, request, *args, **kwargs):
        search = request.POST.get('search')
        if search:
            jednostki = self.get_queryset(). \
                filter(nazwa__icontains=search)
        else:
            jednostki = self.get_queryset()

        paginator = Paginator(jednostki, 10)
        page = self.request.GET.get('page')
        try:
            jednostki = paginator.page(page)
        except PageNotAnInteger:
            jednostki = paginator.page(1)
        except EmptyPage:
            jednostki = paginator.page(paginator.num_pages)
        context = {
            'jednostki': jednostki,
            'search': search,
        }
        return render(request, self.template_name, context)


class JednostkaDetailView(DetailView):
    model = JednOrg
    template_name = 'user_app/jednostka_detail.html'
    context_object_name = 'jednostka'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.object.czy_labi:
            labi = Labi.objects.get(jednostka=self.object.id)
        else:
            labi = None
        context['labi'] = labi
        return context


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
                if historia.status == '5':
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
        if historia.status == '2':
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
    jednostki = JednOrg.objects.all().order_by('nazwa')

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
            if jednostka:
                jednostka = JednOrg.objects.get(id=jednostka)
            else:
                messages.warning(request, 'Najpierw wybierz jednostkę')
            obj_list = Obiekt.objects.filter(
                jedn_org=jednostka,
                nazwa__icontains=szukaj_obiektu,
            )

        if request.POST.get('clear'):
            cart.obiekty.clear()

        if request.POST.get('delete'):
            cart.obiekty.remove(Obiekt.objects.get(id=obj))

        if request.POST.get('add'):
            cart.obiekty.add(Obiekt.objects.get(id=obj))
            jednostka = request.POST.get('jednostka')
            obj_list = Obiekt.objects.filter(jedn_org=jednostka)
            jednostka = JednOrg.objects.get(id=jednostka)

        if request.POST.get('show'):
            jednostka = request.POST.get('jednostka')
            obj_list = Obiekt.objects.filter(jedn_org=jednostka)
            jednostka = JednOrg.objects.get(id=jednostka)

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

    context = {
        'wybrana_jednostka': jednostka,
        'jednostki': jednostki,
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
    jednostki = JednOrg.objects.all().order_by('nazwa')

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
            if jednostka:
                jednostka = JednOrg.objects.get(id=jednostka)
            else:
                messages.warning(request, 'Najpierw wybierz jednostkę')
            prac_list = Pracownik.objects.filter(
                jedn_org=jednostka,
                nazwisko__icontains=szukaj_pracownika,
            )

        if request.POST.get('clear'):
            cart.pracownicy.clear()

        if request.POST.get('delete'):
            cart.pracownicy.remove(Pracownik.objects.get(login=prac))

        if request.POST.get('add'):
            cart.pracownicy.add(Pracownik.objects.get(login=prac))
            jednostka = request.POST.get('jednostka')
            prac_list = Pracownik.objects.filter(jedn_org=jednostka)
            jednostka = JednOrg.objects.get(id=jednostka)

        if request.POST.get('show'):
            jednostka = request.POST.get('jednostka')
            prac_list = Pracownik.objects.filter(jedn_org=jednostka)
            jednostka = JednOrg.objects.get(id=jednostka)

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

    context = {
        'wybrana_jednostka': jednostka,
        'jednostki': jednostki,
        'pracownik': pracownik,
        'prac_list': prac_list,
        'prac_cart': cart.pracownicy.all(),
    }
    return render(request, 'user_app/wizard/step_two.html', context)


def step_three(request):
    pracownik_id = request.session['pracownik']
    pracownik = Pracownik.objects.get(login=pracownik_id)
    cart = Cart.objects.get(id=pracownik_id)
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
            return HttpResponseRedirect('/wizard/step_four')
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
            for pracownik in cart.pracownicy.all():
                w.pracownicy.add(pracownik)
            for obiekt in wniosek['obiekty']:
                w.obiekty.add(obiekt)
            komentarz_id = 'komentarz' + str(wniosek['labi'].id)
            komentarz = request.POST.get(komentarz_id)
            w.komentarz = komentarz
            w.save()
        cart.delete()
        return HttpResponseRedirect('/user_index')
    context = {
        'wnioski': wnioski,
        'pracownik': pracownik,
        'cart': cart,
    }
    return render(request, 'user_app/wizard/step_four.html', context)


def admin_panel(request):
    pracownik_id = request.session['pracownik']
    pracownik = Pracownik.objects.get(login=pracownik_id)
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
