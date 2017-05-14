from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib import auth
from .models import Pracownik, Wniosek, Obiekt
from .forms import WniosekForm
from django.utils import formats
from django.contrib.auth.forms import UserCreationForm


def index(request):

    # import pdb
    # pdb.set_trace()

    template = "wnioski/index.html"
    context = {}
    return render(request, template, context)


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
    template = "wnioski/login.html"
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


def loggedin(request):
    return render(request, 'wnioski/loggedin.html', {'username': request.user.username})


def logout(request):
    auth.logout(request)
    return render(request, 'wnioski/logout.html', {})


def invalid(request):
    return render(request, 'wnioski/invalid.html', {})


def create_user(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/acc/create_user_succ')
        else:
            return HttpResponseRedirect('/acc/create_user_error')
    args = {}
    args['form'] = UserCreationForm()
    return render(request, 'wnioski/create_user.html', args)


def create_user_succ(request):
    return render(request, 'wnioski/create_user_succ.html', {})


def create_user_error(request):
    return render(request, 'wnioski/create_user_error.html', {})
