# -*- coding: utf-8 -*-
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views.generic import ListView, DetailView

from auth_ex.forms import JednostkaForm
from auth_ex.views import find_labi
from .forms import (
    WniosekForm,
    ObiektForm,
    TypeForm,
    EditObiektForm,
    EditWniosekForm)
from .forms import EditTypObiektuForm
from .models import (
    Wniosek,
    Obiekt,
    Historia,
    TypObiektu,
    ZatwierdzonePrzezAS,
)
from auth_ex.models import JednOrg, Pracownik, Labi


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
        wnioski = Wniosek.objects.all()
        wnioski_pracownika = []
        for wniosek in wnioski:
            for prac_wniosek in wniosek.pracownicy.all():
                if prac_wniosek.pk == self.object.pk:
                    wnioski_pracownika.append(wniosek)

        obiekty = ZatwierdzonePrzezAS.objects.filter(
            wniosek__in=wnioski_pracownika,
        )

        context['historie'] = historie
        context['obiekty'] = obiekty
        return context


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
        context = {
            'obiekty': obiekty,
            'search': search,
        }
        return render(request, self.template_name, context)


class ObiektDetailView(DetailView):
    model = Obiekt
    template_name = 'wnioski/obiekt/obiekt_detail.html'
    context_object_name = 'obiekt'


def create_app(request):
    if request.method == 'POST':
        form = WniosekForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('wnioski/create/create_app.html')
    else:
        form = WniosekForm()

    template = "wnioski/create/create_app.html"
    context = {'form': form}
    return render(request, template, context)


def typy_obiektow(request):
    typy_obiektow = TypObiektu.objects.all()
    template = "wnioski/views/typy_obiektow.html"
    context = {'typy_obiektow': typy_obiektow}
    return render(request, template, context)


def jednostki(request):
    jednostki = JednOrg.objects.order_by('id')
    template = "wnioski/views/jednostki.html"
    context = {'jednostki': jednostki}
    return render(request, template, context)


def user_account(request):
    if request.user.is_authenticated():
        session_user = request.session['session_user']
        user = User.objects.get(id=session_user)
        return render(request, 'wnioski/user/user_account.html', {
            'user': user})


def typ_obiektu_view(request, typ_obiektu_id):
    typ_obiektu = TypObiektu.objects.get(id=typ_obiektu_id)
    return render(request, 'wnioski/views/typ_obiektu_view.html', {
        'typ_obiektu': typ_obiektu})


def jednostka_view(request, pk):
    jednostka = JednOrg.objects.get(pk=pk)
    if jednostka.czy_labi:
        try:
            labi = Labi.objects.get(jednostka=pk)
        except Labi.DoesNotExist:
            labi = find_labi(pk)
    else: 
        labi = find_labi(pk)

    return render(request, 'wnioski/views/jednostka_view.html', {
        'jednostka': jednostka,
        'labi': labi,
    })


def create_user(request):
    message = ''
    if request.method == 'POST':
        form = PracownikForm(request.POST)
        if form.is_valid():
            form.save()
            message = 'Dodano użytkownika'
            form = PracownikForm()
            return render(
                request, 'wnioski/create/create_user.html',
                {'message': message, 'form': form}
            )
    else:
        form = PracownikForm()

    template = "wnioski/create/create_user.html"
    args = {}
    args['form'] = PracownikForm()
    return render(request, template, args)


def create_obj(request):
    message = ''
    if request.method == 'POST':
        form = ObiektForm(request.POST)
        if form.is_valid():
            form.save()
            message = 'Dodano obiekt'
            form = ObiektForm()
            return render(
                request, 'wnioski/create/create_user.html',
                {'message': message, 'form': form}
            )
    else:
        form = ObiektForm()

    template = "wnioski/create/create_obj.html"
    args = {}
    args['form'] = ObiektForm()
    return render(request, template, args)


def create_type(request):
    message = ''
    if request.method == 'POST':
        form = TypeForm(request.POST)
        if form.is_valid():
            form.save()
            message = 'Dodano typ obiektu'
            form = TypeForm()
            return render(
                request, 'wnioski/create/create_type.html',
                {'message': message, 'form': form}
            )
    else:
        form = TypeForm()

    template = "wnioski/create/create_type.html"
    args = {}
    args['form'] = TypeForm()
    return render(request, template, args)


def create_unit(request):
    template = 'wnioski/create/create_unit.html'
    if request.method == 'POST':
        form = JednostkaForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Dodano pomyślnie')
            return HttpResponseRedirect('/jednostki')
        else:
            messages.error(request, 'Błąd w formularzu')
    else:
        form = JednostkaForm()
    context = {
        'form': form,
    }
    return render(request, template, context)


def user_edit(request, user_id):
    user = Pracownik.objects.get(id=user_id)
    form = EditPracownikForm(request.POST or None, instance=user)
    if request.POST and form.is_valid():
        form.save()
        return HttpResponseRedirect(
            '/user_view/{0}'.format(user_id)
        )
    else:
        form = EditPracownikForm(instance=user)
    return render(request, 'wnioski/edit/user_edit.html', {
        'user': user,
        'form': form
    })


def app_edit(request, app_id):
    wniosek = Wniosek.objects.get(id=app_id)
    form = EditWniosekForm(request.POST or None, instance=wniosek)
    if request.POST and form.is_valid():
        form.save()
        return HttpResponseRedirect(
            '/wniosek_view/{0}'.format(app_id)
        )
    else:
        form = EditWniosekForm(instance=wniosek)
    return render(request, 'wnioski/edit/app_edit.html', {
        'wniosek': wniosek,
        'form': form
    })


def obj_edit(request, obj_id):
    obiekt = Obiekt.objects.get(id=obj_id)
    form = EditObiektForm(request.POST or None, instance=obiekt)
    if request.POST and form.is_valid():
        form.save()
        return HttpResponseRedirect(
            '/obj_view/{0}'.format(obj_id)
        )
    else:
        form = EditObiektForm(instance=obiekt)
    return render(request, 'wnioski/edit/obj_edit.html', {
        'obiekt': obiekt,
        'form': form
    })


def typ_obiektu_edit(request, typ_obiektu_id):
    typ_obiektu = TypObiektu.objects.get(id=typ_obiektu_id)
    form = EditTypObiektuForm(request.POST or None, instance=typ_obiektu)
    if request.POST and form.is_valid():
        form.save()
        return HttpResponseRedirect(
            '/typ_obiektu_view/{0}'.format(typ_obiektu_id)
        )
    else:
        form = EditTypObiektuForm(instance=typ_obiektu)
    return render(request, 'wnioski/edit/typ_obiektu_edit.html', {
        'typ_obiektu': typ_obiektu,
        'form': form
    })


def jednostka_edit(request, jednostka_id):
    jednostka = JednOrg.objects.get(id=jednostka_id)
    form = EditJednostkaForm(request.POST or None, instance=jednostka)
    if request.POST and form.is_valid():
        form.save()
        return HttpResponseRedirect(
            '/jednostka_view/{0}'.format(jednostka_id)
        )
    else:
        form = EditJednostkaForm(instance=jednostka)
    return render(request, 'wnioski/edit/jednostka_edit.html', {
        'jednostka': jednostka,
        'form': form
    })
