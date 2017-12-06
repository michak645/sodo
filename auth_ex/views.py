from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.shortcuts import redirect
from django.urls import reverse, reverse_lazy
from django.views.generic import ListView, DetailView, DeleteView

from auth_ex.forms import PracownikForm
from auth_ex.models import JednOrg


def workspace(request):
    jednostki = JednOrg.objects.all()
    context = {
        'jednostki': jednostki,
    }
    return render(request, 'auth_ex/workspace/workspace.html', context)


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


class UserListView(ListView):
    model = User
    template_name = 'auth_ex/user_list.html'
    context_object_name = 'users'


class UserDetailView(DetailView):
    model = User
    template_name = 'auth_ex/user_detail.html'
    context_object_name = 'user'


def UserUpdateView(request, pk):
    user = User.objects.get(pk=pk)
    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=user)
        pracownik_form = PracownikForm(request.POST, instance=user.pracownik)
        if user_form.is_valid() and pracownik_form.is_valid():
            user_form.save()
            pracownik_form.save()
            messages.success(request, 'User was successfully added')
            return HttpResponseRedirect(reverse('user_detail', kwargs={'pk': pk}))
        else:
            messages.error(request, 'Please correct errors')
    else:
        user_form = UserForm(instance=user)
        pracownik_form = PracownikForm(instance=user.pracownik)
    return render(request, 'auth_ex/user_update.html', {
        'user': user,
        'user_form': user_form,
        'pracownik_form': pracownik_form
    })


class UserDeleteView(DeleteView):
    model = User
    template_name = 'auth_ex/user_delete.html'

    def get_success_url(self):
        return reverse_lazy('user_list')
