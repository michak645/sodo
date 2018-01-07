# -*- coding: utf-8 -*-
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.shortcuts import render, redirect
from django.utils.decorators import method_decorator
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView

from auth_ex.views import find_labi
from .models import (
    Wniosek,
    Obiekt,
    Historia,
    TypObiektu,
    ZatwierdzonePrzezAS,
    PracownicyObiektyUprawnienia,
)
from auth_ex.models import (
    JednOrg,
    Pracownik,
    Labi,
    RodzajPracownika,
)
from user_app.models import Cart
from user_app.forms import WizardUprawnienia


def admin_index(request):
    wnioski = Wniosek.objects.all()
    admin = Labi.objects.get(id=request.session['pracownik'])
    to_approve = []

    for wniosek in wnioski:
        obiekt = wniosek.obiekty.all()[0]
        wniosek_labi = find_labi(obiekt.jedn_org.id)
        if wniosek_labi == admin:
            historia = Historia.objects.filter(
                wniosek=wniosek.id,
            ).order_by('-data')[0]
            if historia.get_status() == 'Złożony':
                to_approve.append(historia)

    context = {
        'admin': admin,
        'wnioski': wnioski,
        'to_approve': to_approve,
    }
    return render(request, 'wnioski/homepage/homepage.html', context)


def wnioski(request):
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
    return render(request, 'wnioski/wniosek/wniosek_list.html', context)


def wniosek_detail(request, pk):
    template = 'wnioski/wniosek/wniosek_detail.html'
    w = Wniosek.objects.get(id=pk)
    # date = datetime.now()
    if request.method == 'POST':
        if request.POST.get('change') == "Zatwierdź":
            Historia.objects.create(
                wniosek_id=pk,
                status='2',
            )
            historia = Historia.objects. \
                filter(wniosek=pk). \
                order_by('-data')

            return HttpResponseRedirect('/admin_index')
        elif request.POST.get('change') == "Odrzuć":
            Historia.objects.create(
                wniosek_id=pk,
                status='5',
            )
            historia = Historia.objects.filter(wniosek=pk)
            return HttpResponseRedirect('/admin_index')
    else:
        historia = Historia.objects. \
            filter(wniosek=pk). \
            order_by('-data')
        status = historia[0].get_status_display()
        return render(request, template, {
            'wniosek': w,
            'historia': historia,
            'status': status
        })


class PracownikListView(ListView):
    model = Pracownik
    template_name = 'wnioski/pracownik/pracownik_list.html'
    context_object_name = 'pracownicy'
    queryset = Pracownik.objects.all().order_by('nazwisko')

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        paginator = Paginator(self.get_queryset(), 10)
        page = self.request.GET.get('page')
        try:
            pracownicy = paginator.page(page)
        except PageNotAnInteger:
            pracownicy = paginator.page(1)
        except EmptyPage:
            pracownicy = paginator.page(paginator.num_pages)
        context['pracownicy'] = pracownicy
        return context

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(PracownikListView, self).dispatch(*args, **kwargs)

    def post(self, request, *args, **kwargs):
        search = request.POST.get('search')
        if search:
            pracownicy = self.get_queryset(). \
                filter(nazwisko__icontains=search)
        else:
            pracownicy = self.get_queryset()
        context = {
            'pracownicy': pracownicy,
            'search': search,
        }
        return render(request, self.template_name, context)


class PracownikDetailView(DetailView):
    model = Pracownik
    template_name = 'wnioski/pracownik/pracownik_detail.html'
    context_object_name = 'pracownik'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        wnioski = Wniosek.objects.filter(
            pracownik=self.object.pk).order_by('-data')
        historie = []
        for wniosek in wnioski:
            try:
                hist = Historia.objects.filter(
                    wniosek=wniosek).order_by('-data')[0]
                historie.append(hist)
            except IndexError:
                hist = None
        wnioski_pracownika = []
        for wniosek in wnioski:
            for prac_wniosek in wniosek.pracownicy.all():
                if prac_wniosek.pk == self.object.pk:
                    wnioski_pracownika.append(wniosek)

        paginator = Paginator(historie, 5)
        page = self.request.GET.get('page')
        try:
            historie = paginator.page(page)
        except PageNotAnInteger:
            historie = paginator.page(1)
        except EmptyPage:
            historie = paginator.page(paginator.num_pages)

        obiekty = ZatwierdzonePrzezAS.objects.filter(
            wniosek__in=wnioski_pracownika,
        )

        context['historie'] = historie
        context['obiekty'] = obiekty
        return context


class PracownikCreate(CreateView):
    model = Pracownik
    fields = ['login', 'imie', 'nazwisko', 'email',
              'rodzaj', 'jedn_org', 'numer_ax']
    template_name = 'wnioski/pracownik/pracownik_create.html'
    success_url = reverse_lazy('labi_pracownik_list')

    def form_valid(self, form):
        messages.success(self.request, 'Pomyślnie dodano pracownika.')
        return super().form_valid(form)


class RodzajPracownikaCreate(CreateView):
    model = RodzajPracownika
    fields = ['rodzaj', ]
    template_name = 'wnioski/pracownik/rodzaj_pracownika_create.html'
    success_url = reverse_lazy('labi_pracownik_list')

    def form_valid(self, form):
        messages.success(self.request, 'Pomyślnie dodano rodzaj pracownika.')
        return super().form_valid(form)


class ObiektListView(ListView):
    model = Obiekt
    template_name = 'wnioski/obiekt/obiekt_list.html'
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
    template_name = 'wnioski/obiekt/obiekt_detail.html'
    context_object_name = 'obiekt'


class ObiektCreate(CreateView):
    model = Obiekt
    fields = ['nazwa', 'typ', 'jedn_org', 'opis']
    template_name = 'wnioski/obiekt/obiekt_create.html'
    success_url = reverse_lazy('labi_obiekt_list')

    def form_valid(self, form):
        messages.success(self.request, 'Pomyślnie dodano obiekt.')
        return super().form_valid(form)


class ObiektTypCreate(CreateView):
    model = TypObiektu
    fields = ['nazwa', ]
    template_name = 'wnioski/obiekt/obiekt_typ_create.html'
    success_url = reverse_lazy('labi_obiekt_list')

    def form_valid(self, form):
        messages.success(self.request, 'Pomyślnie dodano typ obiektu.')
        return super().form_valid(form)


class JednostkaListView(ListView):
    model = JednOrg
    template_name = 'wnioski/jednostka/jednostka_list.html'
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
    template_name = 'wnioski/jednostka/jednostka_detail.html'
    context_object_name = 'jednostka'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.object.czy_labi:
            labi = Labi.objects.get(jednostka=self.object.id)
        else:
            labi = None
        context['labi'] = labi
        return context


class JednostkaCreate(CreateView):
    model = JednOrg
    fields = ['nazwa', 'parent', 'czy_labi']
    template_name = 'wnioski/jednostka/jednostka_create.html'
    success_url = reverse_lazy('labi_jednostka_list')

    def form_valid(self, form):
        messages.success(self.request, 'Pomyślnie dodano jednostkę.')
        return super().form_valid(form)


def step_one(request):
    pracownik_id = request.session['pracownik']
    pracownik = Pracownik.objects.get(login=pracownik_id)
    cart, created = Cart.objects.get_or_create(id=pracownik_id)
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
    return render(request, 'wnioski/wizard/step_one.html', context)


def step_two(request):
    pracownik_id = request.session['pracownik']
    pracownik = Pracownik.objects.get(login=pracownik_id)
    cart = Cart.objects.get(id=pracownik_id)
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
    return render(request, 'wnioski/wizard/step_two.html', context)


def step_three(request):
    # czy_chcesz_zostac_dodany_do_wnioski_checkbox = False
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
        form = WizardUprawnienia()
    context = {
        'pracownik': pracownik,
        'cart': cart,
        'aktualne_uprawnienia': aktualne_uprawnienia,
        'form': form,
        'obiekty': obiekty,
    }
    return render(request, 'wnioski/wizard/step_three.html', context)


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
        return redirect('admin_index')
    context = {
        'wnioski': wnioski,
        'pracownik': pracownik,
        'cart': cart,
    }
    return render(request, 'wnioski/wizard/step_four.html', context)
