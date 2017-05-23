from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib import auth
from .models import Pracownik, Wniosek, Obiekt
from .forms import WniosekForm, SearchForm, PracownikForm
from django.utils import formats
from django.contrib.auth.decorators import login_required


def index(request):

    # import pdb
    # pdb.set_trace()

    template = "wnioski/index.html"
    context = {}
    return render(request, template, context)


@login_required(login_url='/')
def add(request):

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
    else:
        form = WniosekForm()

    template = "wnioski/add.html"
    context = {'form': form, 'thanks': thanks}
    return render(request, template, context)


@login_required(login_url='/')
def create_user(request):
    if request.method == 'POST':
        form = PracownikForm(request.POST)
        if form.is_valid():
            form.save()
    else:
        form = PracownikForm()

    template = "wnioski/create_user.html"
    context = {'form': form}
    return render(request, template, context)


@login_required(login_url='/')
def list(request):

    pracownik = Pracownik.objects.all()
    obiekt = Obiekt.objects.all()
    wniosek = Wniosek.objects.order_by('-data_zlo')[:5]

    template = "wnioski/list.html"

    context = {
        'pracownik': pracownik,
        'obiekt': obiekt,
        'wniosek': wniosek
    }
    return render(request, template, context)


def login(request):
    template = "wnioski/index.html"
    context = {}
    return render(request, template, context)


def authentication(request):
    username = request.POST.get('username', '')
    password = request.POST.get('password', '')
    user = auth.authenticate(username=username, password=password)

    if user is not None:
        auth.login(request, user)
        return HttpResponseRedirect('/acc/loggedin/')
    else:
        return HttpResponseRedirect('/acc/invalid/')


@login_required(login_url='/')
def loggedin(request):
    return render(request, 'wnioski/loggedin.html', {
        'username': request.user.username}
    )


def logout(request):
    auth.logout(request)
    return render(request, 'wnioski/logout.html', {})


def invalid(request):
    return render(request, 'wnioski/invalid.html', {})


def create_user_succ(request):
    return render(request, 'wnioski/create_user_succ.html', {})


def create_user_error(request):
    return render(request, 'wnioski/create_user_error.html', {})


@login_required(login_url='/')
def search(request):

    if request.method == 'GET':
        username = SearchForm(request.GET)
        if username.is_valid():
            user = username.cleaned_data['username'].encode('utf-8').strip()
            message = 'Wyszukiwanie dla: "{0}"'.format(
                user
            )
            pracownicy = Pracownik.objects.filter(nazwisko__icontains=user)
            return render(request, 'wnioski/search_results.html', {
                'pracownicy': pracownicy, 'message': message}
            )
    else:
        username = SearchForm()
        message = "cos nie tak.. {0}".format(username)
        return render(request, 'wnioski/search_results.html', {
            'message': message, 'username': username}
        )

    return render(request, 'wnioski/search.html')


@login_required(login_url='/')
def user_view(request, user_id):
    pracownik = Pracownik.objects.get(id=user_id)
    return render(request, 'wnioski/user_view.html', {
        'pracownik': pracownik})


@login_required(login_url='/')
def user_account(request):
    if request.user.is_authenticated():
        return render(request, 'wnioski/user_account.html', {
            'user': request.user})
