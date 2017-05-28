from django.shortcuts import render
from .models import Pracownik, Wniosek, Obiekt
from .forms import WniosekForm, SearchForm
from django.utils import formats
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.contrib import auth
from django.contrib.auth.forms import UserCreationForm
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

    pracownicy = Pracownik.objects.all()
    obiekt = Obiekt.objects.all()
    wniosek = Wniosek.objects.order_by('-data_zlo')[:5]

    template = "wnioski/views/list.html"

    context = {
        'pracownicy': pracownicy,
        'obiekt': obiekt,
        'wniosek': wniosek
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
def user_view(request, user_id):
    pracownik = Pracownik.objects.get(id=user_id)
    session_user = request.session['session_user']
    user = User.objects.get(id=session_user)
    return render(request, 'wnioski/views/user_view.html', {
        'pracownik': pracownik}, {'user': user})


@login_required(login_url='/')
def user_account(request):
    if request.user.is_authenticated():
        session_user = request.session['session_user']
        user = User.objects.get(id=session_user)
        return render(request, 'wnioski/user/user_account.html', {
            'user': user})


@login_required(login_url='/')
def obj_view(request, obj_id):
    obiekt = Obiekt.objects.get(id=obj_id)
    return render(request, 'wnioski/views/obj_view.html', {
        'obiekt': obiekt})


@login_required(login_url='/')
def wniosek_view(request, wniosek_id):
    wniosek = Wniosek.objects.get(id=wniosek_id)
    return render(request, 'wnioski/views/wniosek_view.html', {
        'wniosek': wniosek})


@login_required(login_url='/')
def create_user(request):
    message = ''
    if request.method == 'POST':
        form1 = PracownikForm(request.POST)
        form2 = UserCreationForm(request.POST)
        if (form1.is_valid() and form2.is_valid):
            form1.save()
            form2.save()
            message = 'Dodano użytkownika'
            form1 = PracownikForm()
            form2 = UserCreationForm()
            return render(
                request, 'wnioski/create/create_user.html',
                {'message': message, 'form1': form1, 'form2': form2}
            )
    else:
        form1 = PracownikForm()
        form2 = UserCreationForm()

    template = "wnioski/create/create_user.html"
    args = {}
    args['form2'] = UserCreationForm()
    args['form1'] = PracownikForm()
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
        return HttpResponseRedirect('/acc/loggedin/')
    else:
            return HttpResponseRedirect('/acc/invalid/')


@login_required(login_url='/')
def loggedin(request):
    session_user = request.session['session_user']
    user = User.objects.get(id=session_user)
    return render(request, 'wnioski/user/loggedin.html', {
        'username': user.username}
    )


def logout(request):
    auth.logout(request)
    return render(request, 'wnioski/user/logout.html', {})


def invalid(request):
    return render(request, 'wnioski/user/invalid.html', {})
