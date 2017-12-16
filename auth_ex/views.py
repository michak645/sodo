from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.shortcuts import redirect
from django.urls import reverse, reverse_lazy
from django.views.generic import ListView, DetailView, DeleteView

from auth_ex.forms import PracownikForm
from auth_ex.models import JednOrg, Labi, Pracownik


def find_labi(jedn):
    jednostka = JednOrg.objects.get(id=jedn)
    if jednostka.czy_labi:
        return Labi.objects.get(jednostka=jednostka.id)
    else:
        return find_labi(jednostka.parent.id)


def workspace(request):
    jednostki = JednOrg.objects.all().order_by('id')
    adminy = Labi.objects.all()
    context = {
        'jednostki': jednostki,
        'adminy': adminy,
    }
    if request.method == 'POST':
        jednostka = request.POST['jedn']
        try:
            jedn = JednOrg.objects.get(id=jednostka)
            messages.success(request, 'Success')
        except Labi.DoesNotExist:
            jedn = None
            messages.error(request, 'Error')

        if jedn:
            parent = find_labi(jedn.id)

        context['jedn'] = jedn
        context['parent'] = parent
        return render(request, 'auth_ex/workspace/workspace.html', context)

    return render(request, 'auth_ex/workspace/workspace.html', context)


def index(request):
    if request.method == 'POST':
        login = request.POST['login']
        try:
            admin = Labi.objects.get(login=login)
            request.session['admin'] = admin.id
        except Labi.DoesNotExist:
            admin = None
        if admin is None:
            try:
                pracownik = Pracownik.objects.get(login=login)
                request.session['pracownik'] = pracownik.login
            except Pracownik.DoesNotExist:
                admin = None
                pracownik = None

        if admin:
            messages.success(request, 'success')
            return redirect('wnioski')
        elif pracownik:
            messages.success(request, 'success')
            return redirect('user_index')
        else:
            messages.error(request, 'error')
            return redirect('index')
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
