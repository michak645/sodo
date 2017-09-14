# -*- coding: utf-8 -*-
from django.shortcuts import render
from .models import Pracownik, Wniosek, Obiekt, Historia, TypObiektu, JednOrg
from .forms import (
    WniosekForm, SearchForm, ObiektForm, TypeForm,
    EditObiektForm, EditWniosekForm)
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.contrib import auth
from .forms import (
    PracownikForm, EditPracownikForm, EditTypObiektuForm, JednostkaForm,
    EditJednostkaForm)
from datetime import datetime


@login_required(login_url='/')
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


@login_required(login_url='/')
def pracownicy(request):
    pracownicy = Pracownik.objects.all()
    template = "wnioski/views/pracownicy.html"
    context = {'pracownicy': pracownicy}
    return render(request, template, context)


@login_required(login_url='/')
def obiekty(request):
    obiekty = Obiekt.objects.all()
    template = "wnioski/views/obiekty.html"
    context = {'obiekty': obiekty}
    return render(request, template, context)


@login_required(login_url='/')
def wnioski(request):
    wnioski = Wniosek.objects.all()
    historie = Historia.objects.all().order_by('-data')

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

    template = "wnioski/views/wnioski.html"
    context = {
        'wnioski': wnioski,
        'historie': historie,
        'przyjete': przyjete,
        'odrzucone': odrzucone,
        'przetwarzane': przetwarzane,
    }
    return render(request, template, context)


@login_required(login_url='/')
def typy_obiektow(request):
    typy_obiektow = TypObiektu.objects.all()
    template = "wnioski/views/typy_obiektow.html"
    context = {'typy_obiektow': typy_obiektow}
    return render(request, template, context)


@login_required(login_url='/')
def jednostki(request):
    jednostki = JednOrg.objects.order_by('nazwa')
    template = "wnioski/views/jednostki.html"
    context = {'jednostki': jednostki}
    return render(request, template, context)


@login_required(login_url='/')
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


@login_required(login_url='/')
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
                max_id = Historia.objects.filter(wniosek=w.id).aggregate(id=Max('id'))['id']
                historia = Historia.objects.get(wniosek=w.id, id=max_id)
            except Historia.DoesNotExist:
                historie = None
            if historia is not None and w.typ_id == 4 and historia.status_id == 5:
                obiekt = Obiekt.objects.get(id=w.obiekt_id)
                obiekty.append(obiekt)
        return render(request, 'wnioski/user/user_account.html', {
            'user': user, 'obiekty': obiekty})
    '''


@login_required(login_url='/')
def user_view(request, user_id):
    pracownicy = Pracownik.objects.get(id=user_id)
    wnioski = Wniosek.objects.filter(pracownik=user_id)
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
    context = {
        'pracownik': pracownicy,
        'wnioski': wnioski,
        'przyjete': przyjete,
        'odrzucone': odrzucone,
        'przetwarzane': przetwarzane,
    }
    return render(request, 'wnioski/views/user_view.html', context)


@login_required(login_url='/')
def obj_view(request, obj_id):
    obiekt = Obiekt.objects.get(id=obj_id)
    return render(request, 'wnioski/views/obj_view.html', {
        'obiekt': obiekt})


@login_required(login_url='/')
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
                historia = Historia.objects.filter(wniosek=wniosek_id).order_by('-data')
            except Historia.DoesNotExist:
                historia = None
            return render(request, 'wnioski/views/wniosek_view.html', {
                    'wniosek': w,
                    'historia': historia,
                    'message': message,
                    'date': date, })
        elif request.POST.get('change', '') == u"Odrzuć":
            historia = Historia(wniosek_id=wniosek_id, status='2')
            historia.save()
            message = 'Odrzucono wniosek'
            try:
                historia = Historia.objects.filter(wniosek=wniosek_id)
            except Historia.DoesNotExist:
                historia = None
            return render(request, 'wnioski/views/wniosek_view.html', {
                'wniosek': w, 'historia': historia, 'message': message, 'date': date})    

    else:
        try:
            historia = Historia.objects.filter(wniosek=wniosek_id).order_by('-data')
            status = historia[0].status
        except Historia.DoesNotExist:
            historia = None
        return render(request, 'wnioski/views/wniosek_view.html', {
            'wniosek': w,
            'historia': historia,
            'status': status,
        })


@login_required(login_url='/')
def typ_obiektu_view(request, typ_obiektu_id):
    typ_obiektu = TypObiektu.objects.get(id=typ_obiektu_id)
    return render(request, 'wnioski/views/typ_obiektu_view.html', {
        'typ_obiektu': typ_obiektu})


@login_required(login_url='/')
def jednostka_view(request, jednostka_id):
    jednostka = JednOrg.objects.get(id=jednostka_id)
    return render(request, 'wnioski/views/jednostka_view.html', {
        'jednostka': jednostka})


@login_required(login_url='/')
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


@login_required(login_url='/')
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


@login_required(login_url='/')
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


@login_required(login_url='/')
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


def login(request):
    request.session['ldap_user'] = None
    template = "wnioski/index.html"
    context = {}
    return render(request, template, context)


def authentication(request):
    username = request.POST.get('username', '')
    password = request.POST.get('password', '')
    user_auth = auth.authenticate(username=username, password=password)

    if user_auth is not None:

        auth.login(request, user_auth)
        request.session['session_user'] = user_auth.id
        return HttpResponseRedirect('/wnioski')
    else:
            return HttpResponseRedirect('/acc/invalid/')


def logout(request):
    auth.logout(request)
    return render(request, 'wnioski/user/logout.html', {})


def invalid(request):
    return render(request, 'wnioski/user/invalid.html', {})


@login_required(login_url='/')
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


@login_required(login_url='/')
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


@login_required(login_url='/')
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


@login_required(login_url='/')
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


@login_required(login_url='/')
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


def ldap_login(request):
    template = 'wnioski/ldap/login.html'
    context = {
        'pracownicy': Pracownik.objects.all(),
    }
    return render(request, template, context)


# do zrobienia
def ldap_auth(request):
    username = ''
    username = request.POST.get('username', '')
    request.session['ldap_user'] = username
    try:
        user_auth = Pracownik.objects.get(login=username)
        user_auth.id
        return HttpResponseRedirect('/ldap/main')
    except Pracownik.DoesNotExist:
        user_auth = None
        return HttpResponseRedirect('/ldap/login')


def ldap_main(request):
    ldap_user = request.session['ldap_user']
    try:
        user = Pracownik.objects.get(login=ldap_user)
    except Pracownik.DoesNotExist:
        return HttpResponseRedirect('/ldap/login')
    message = ''
    user = Pracownik.objects.get(login=ldap_user)
    wnioski = Wniosek.objects.filter(pracownik=user).order_by('-data')

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

    if request.method == 'POST':
        form = WniosekForm(request.POST)
        if form.is_valid():
            form.save()
            form = WniosekForm()
            message = 'wniosek dodany'
            template = "wnioski/ldap/main.html"
            return render(request, template, {
                'form': form,
                'message': message,
                'user': user,
                'wnioski': wnioski,
                'przyjete': przyjete,
                'odrzucone': odrzucone,
                'przetwarzane': przetwarzane,
            })
    else:
        form = WniosekForm()
        template = "wnioski/ldap/main.html"
        return render(request, template, {
            'form': form,
            'message': message,
            'user': user,
            'wnioski': wnioski,
            'przyjete': przyjete,
            'odrzucone': odrzucone,
            'przetwarzane': przetwarzane,
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


def ldap_logout(request):
    request.session['ldap_user'] = ''
    return HttpResponseRedirect('/ldap/login')
# ========================================================================
