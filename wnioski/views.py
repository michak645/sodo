from django.shortcuts import render
from .models import Pracownik, Wniosek, Obiekt, Historia
from .forms import WniosekForm, SearchForm, ObiektForm
from django.utils import formats
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.contrib import auth
from .forms import PracownikForm


@login_required(login_url='/')
def create_app(request):

    thanks = ''

# thanks = 'dzieki {0}'.format(form.cleaned_data['imie'])

    if request.method == 'POST':
        form = WniosekForm(request.POST)
        if form.is_valid():
            form.save()
            thanks = 'wniosek dodany w dniu {0}'.format(
                formats.date_format(
                    form.cleaned_data['data_zlo'],
                    "SHORT_DATETIME_FORMAT"
                )
            )
            return HttpResponseRedirect('wnioski/create/create_app.html')
    else:
        form = WniosekForm()

    template = "wnioski/create/create_app.html"
    context = {'form': form, 'thanks': thanks}
    return render(request, template, context)


@login_required(login_url='/')
def list(request):
    session_user = request.session['session_user']
    user = User.objects.get(id=session_user)

    pracownicy = Pracownik.objects.all()
    obiekt = Obiekt.objects.all()
    wniosek = Wniosek.objects.order_by('-data_zlo')[:5]

    template = "wnioski/views/list.html"

    context = {
        'pracownicy': pracownicy,
        'obiekt': obiekt,
        'wniosek': wniosek,
        'user': user
    }
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


@login_required(login_url='/')
def user_view(request, user_id):
    pracownik = Pracownik.objects.get(id=user_id)
    wnioski = Wniosek.objects.filter(prac_sklada=user_id)
    return render(request, 'wnioski/views/user_view.html', {
        'pracownik': pracownik, 'wnioski': wnioski})


@login_required(login_url='/')
def obj_view(request, obj_id):
    obiekt = Obiekt.objects.get(id=obj_id)
    return render(request, 'wnioski/views/obj_view.html', {
        'obiekt': obiekt})


# ========================================================================
@login_required(login_url='/')
def wniosek_view(request, wniosek_id):
    wniosek = Wniosek.objects.get(id=wniosek_id)
    try:
        historia = Historia.objects.get(wniosek=wniosek)
    except Historia.DoesNotExist:
        historia = None
    return render(request, 'wnioski/views/wniosek_view.html', {
        'wniosek': wniosek, 'historia': historia})
# ========================================================================


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


def login(request):
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
        return HttpResponseRedirect('/list/')
    else:
            return HttpResponseRedirect('/acc/invalid/')


def logout(request):
    auth.logout(request)
    return render(request, 'wnioski/user/logout.html', {})


def invalid(request):
    return render(request, 'wnioski/user/invalid.html', {})
