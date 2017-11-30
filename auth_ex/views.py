from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
# from django.contrib.auth.models import User
from django.shortcuts import render
from django.shortcuts import redirect


def index(request):
    user = request.user
    if user.is_authenticated:
        if user.is_staff:
            return redirect('/wnioski/')
        else:
            return redirect('ldap/main')
    return render(request, 'auth_ex/index.html')


def auth_view(request):
    username = request.POST.get('username')
    password = request.POST.get('password')
    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        if user.is_staff:
            return redirect('/wnioski/')
        else:
            return redirect('/ldap/main')
    else:
        messages.add_message(request, messages.ERROR, 'login error')
        return render(request, 'auth_ex/index.html')


def logout_view(request):
    messages.add_message(request, messages.INFO, 'logout succesful')
    logout(request)
    return redirect('/')
