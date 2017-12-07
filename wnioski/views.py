# -*- coding: utf-8 -*-
import pdb

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views.generic import ListView, DetailView
from datetime import datetime

from auth_ex.views import find_labi
from .forms import (
    WniosekForm,
    SearchForm,
    ObiektForm,
    TypeForm,
    EditObiektForm,
    EditWniosekForm)
from .forms import EditTypObiektuForm
from .models import Wniosek, Obiekt, Historia, TypObiektu
from auth_ex.models import JednOrg, Pracownik, Labi


# WNIOSKI
def wnioski(request):
    wnioski = Wniosek.objects.all()
    admin_id = request.session['admin']
    admin = Labi.objects.get(id=admin_id)
    to_approve = []
    for wniosek in wnioski:
        wniosek_labi = find_labi(wniosek.obiekt.jedn_org.id)
        if wniosek_labi == admin:
            to_approve.append(wniosek)

    # historie = Historia.objects.all().order_by('-data')
    # przyjete = []
    # odrzucone = []
    # przetwarzane = []
    # for wniosek in wnioski:
    #     try:
    #         hist = Historia.objects.filter(
    #             wniosek=wniosek).order_by('-data')[0]
    #         if hist.status == '1':
    #             przyjete.append(hist)
    #         elif hist.status == '2':
    #             odrzucone.append(hist)
    #         elif hist.status == '3':
    #             przetwarzane.append(hist)
    #     except IndexError:
    #         hist = None

    context = {
        'admin': admin,
        'wnioski': wnioski,
        'to_approve': to_approve,
        # 'historie': historie,
        # 'przyjete': przyjete,
        # 'odrzucone': odrzucone,
        # 'przetwarzane': przetwarzane,
    }
    return render(request, 'wnioski/wniosek/wniosek_list.html', context)


# LIST VIEWS
class PracownikListView(ListView):
    model = Pracownik
    template_name = 'wnioski/views/pracownicy.html'
    context_object_name = 'pracownicy'

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(PracownikListView, self).dispatch(*args, **kwargs)


class PracownikDetailView(DetailView):
    model = Pracownik
    template_name = 'wnioski/views/user_view.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        wnioski = Wniosek.objects.filter(pracownik=self.object.id)
        przyjete = []
        odrzucone = []
        przetwarzane = []
        for wniosek in wnioski:
            try:
                hist = Historia.objects.filter(
                    wniosek=wniosek).order_by('-data')[0]
                if hist.status == '1':
                    przyjete.append(hist)
                elif hist.status == '2':
                    odrzucone.append(hist)
                elif hist.status == '3':
                    przetwarzane.append(hist)
            except IndexError:
                hist = None
        context['wnioski'] = wnioski
        context['przyjete'] = przyjete
        context['odrzucone'] = odrzucone
        context['przetwarzane'] = przetwarzane
        return context


def obiekty(request):
    obiekty = Obiekt.objects.all()
    template = "wnioski/views/obiekty.html"
    context = {'obiekty': obiekty}
    return render(request, template, context)


class ObiektListView(ListView):
    model = Obiekt
    template = 'wnioski/views/obiekty.html'
    context_object_name = 'obiekty'


# CREATING VIEWS
def create_app(request):
    thanks = ''
    # thanks = 'dzieki {0}'.format(form.cleaned_data['imie'])
    if request.method == 'POST':
        form = WniosekForm(request.POST)
        if form.is_valid():
            form.save()
            thanks = 'Wniosek dodany.'
            return HttpResponseRedirect('wnioski/create/create_app.html')
    else:
        form = WniosekForm()

    template = "wnioski/create/create_app.html"
    context = {'form': form, 'thanks': thanks}
    return render(request, template, context)


def typy_obiektow(request):
    typy_obiektow = TypObiektu.objects.all()
    template = "wnioski/views/typy_obiektow.html"
    context = {'typy_obiektow': typy_obiektow}
    return render(request, template, context)


def jednostki(request):
    jednostki = JednOrg.objects.order_by('nazwa')
    template = "wnioski/views/jednostki.html"
    context = {'jednostki': jednostki}
    return render(request, template, context)


def search(request):

    if request.method == 'GET':
        username = SearchForm(request.GET)
        if username.is_valid():
            user = username.cleaned_data['username']
            message = u'dla: "{0}"'.format(
                user
            )
            pracownicy = Pracownik.objects.filter(nazwisko__icontains=user)
            return render(request, 'wnioski/search/search_results.html', {
                'pracownicy': pracownicy, 'message': message}
            )

    else:
        username = SearchForm()
        message = "cos nie tak.. {0}".format(username)
        return render(request, 'wnioski/search/search_results.html', {
            'message': message, 'username': username}
        )

    return render(request, 'wnioski/search/search.html')


def user_account(request):
    if request.user.is_authenticated():
        session_user = request.session['session_user']
        user = User.objects.get(id=session_user)
        return render(request, 'wnioski/user/user_account.html', {
            'user': user})

    '''
    if request.user.is_authenticated():
        session_user = request.session['session_user']
        user = User.objects.get(id=session_user)
        pracownik = Pracownik.objects.get(login=user)
        wnioski = Wniosek.objects.filter(prac_dot=pracownik.id)
        obiekty = []

        for w in wnioski:
            try:
                max_id = Historia.objects.filter(wniosek=w.id).a
                ggregate(id=Max('id'))['id']
                historia = Historia.objects.get(wniosek=w.id, id=max_id)
            except Historia.DoesNotExist:
                historie = None
            if historia is not None and w.typ_id == 4 
            and historia.status_id == 5:
                obiekt = Obiekt.objects.get(id=w.obiekt_id)
                obiekty.append(obiekt)
        return render(request, 'wnioski/user/user_account.html', {
            'user': user, 'obiekty': obiekty})
    '''


def obj_view(request, obj_id):
    obiekt = Obiekt.objects.get(id=obj_id)
    return render(request, 'wnioski/views/obj_view.html', {
        'obiekt': obiekt})


def wniosek_view(request, wniosek_id):
    w = Wniosek.objects.get(id=wniosek_id)
    message = ''
    date = datetime.now()
    if request.method == 'POST':
        if request.POST.get('change', '') == u"Zatwierdź":
            historia = Historia(wniosek_id=wniosek_id, status='1')
            historia.save()
            message = 'Zatwierdzono wniosek'
            try:
                historia = Historia.objects. \
                    filter(wniosek=wniosek_id). \
                    order_by('-data')
            except Historia.DoesNotExist:
                historia = None
            context = {
                'wniosek': w,
                'historia': historia,
                'message': message,
                'date': date,
            }
            return render(request,
                          'wnioski/views/templates/wnioski/wniosek/wniosek_detail.html', context)
        elif request.POST.get('change', '') == u"Odrzuć":
            historia = Historia(wniosek_id=wniosek_id, status='2')
            historia.save()
            message = 'Odrzucono wniosek'
            try:
                historia = Historia.objects.filter(wniosek=wniosek_id)
            except Historia.DoesNotExist:
                historia = None
            context = {
                'wniosek': w,
                'historia': historia,
                'message': message,
                'date': date
            }
            return render(request,
                          'wnioski/views/templates/wnioski/wniosek/wniosek_detail.html', context)

    else:
        try:
            historia = Historia.objects. \
                filter(wniosek=wniosek_id). \
                order_by('-data')
            status = historia[0].status
        except Historia.DoesNotExist:
            historia = None
        return render(request,
                      'wnioski/views/templates/wnioski/wniosek/wniosek_detail.html', {
            'wniosek': w,
            'historia': historia,
            'status': status
        })


def typ_obiektu_view(request, typ_obiektu_id):
    typ_obiektu = TypObiektu.objects.get(id=typ_obiektu_id)
    return render(request, 'wnioski/views/typ_obiektu_view.html', {
        'typ_obiektu': typ_obiektu})


def jednostka_view(request, jednostka_id):
    jednostka = JednOrg.objects.get(id=jednostka_id)
    return render(request, 'wnioski/views/jednostka_view.html', {
        'jednostka': jednostka})


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
    message = ''
    if request.method == 'POST':
        form = JednostkaForm(request.POST)
        if form.is_valid():
            form.save()
            message = 'Dodano jednostkę organizacyjną'
            form = JednostkaForm()
            return render(
                request, 'wnioski/create/create_unit.html',
                {'message': message, 'form': form}
            )
    else:
        form = JednostkaForm()

    template = "wnioski/create/create_unit.html"
    args = {}
    args['form'] = JednostkaForm()
    return render(request, template, args)


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


def obj_list(request):
    ldap_user = request.session['ldap_user']
    try:
        Pracownik.objects.get(login=ldap_user)
    except Pracownik.DoesNotExist:
        return HttpResponseRedirect('/ldap/login')
    obiekty = Obiekt.objects.all()
    template = 'wnioski/ldap/obj_list.html'
    return render(request, template, {
        'obiekty': obiekty
    })


def wniosek_view_ldap(request, wniosek_id):
    ldap_user = request.session['ldap_user']
    try:
        Pracownik.objects.get(login=ldap_user)
    except Pracownik.DoesNotExist:
        return HttpResponseRedirect('/ldap/login')
    wniosek = Wniosek.objects.get(id=wniosek_id)
    return render(request, 'wnioski/ldap/wniosek_view_ldap.html', {
        'wniosek': wniosek})


def ldap_main(request):
    user = request.user
    wnioski = Wniosek.objects.filter(user=user)
    historia = Historia.objects.filter(wniosek__in=wnioski)
    template = "wnioski/ldap/main.html"
    return render(request, template, {
        'user': user,
        'historia': historia,
    })

    # przyjete = []
    # odrzucone = []
    # przetwarzane = []
    # for wniosek in wnioski:
    #     try:
    #         hist = Historia.objects.filter(
    #             wniosek=wniosek).order_by('-data')[0]
    #         if hist.status == '1':
    #             przyjete.append(hist)
    #         elif hist.status == '2':
    #             odrzucone.append(hist)
    #         elif hist.status == '3':
    #             przetwarzane.append(hist)
    #     except IndexError:
    #         hist = None

    # if request.method == 'POST':
    #     form = WniosekForm(request.POST)
    #     if form.is_valid():
    #         form.save()
    #         form = WniosekForm()
    #         message = 'wniosek dodany'
    #         template = "wnioski/ldap/main.html"
    #         return render(request, template, {
    #             'form': form,
    #             'message': message,
    #             'user': user,
    #             'wnioski': wnioski,
    #             'przyjete': przyjete,
    #             'odrzucone': odrzucone,
    #             'przetwarzane': przetwarzane,
    #         })
    # else:


def WniosekCreateView(request):
    if request.method == 'POST':
        post = request.POST.copy()
        post['user'] = request.user.id
        form = WniosekForm(post)
        if form.is_valid():
            form.save()
            messages.success(request, 'Successfully add application')
            return HttpResponseRedirect('/ldap/main')
        else:
            messages.error(request, 'There was some errors')
            return HttpResponseRedirect('/ldap/app_add')
    else:
        form = WniosekForm()
        return render(request, 'wnioski/ldap/app_add.html', {
            'form': form,
        })
