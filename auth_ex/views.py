from django.contrib import messages
from django.shortcuts import render
from django.shortcuts import redirect

from auth_ex.models import JednOrg, Labi, Pracownik


def find_labi(jedn):
    jednostka = JednOrg.objects.get(id=jedn)
    if jednostka.czy_labi:
        return Labi.objects.get(jednostka=jednostka.id)
    else:
        return find_labi(jednostka.parent.id)


def index(request):
    if request.method == 'POST':
        login = request.POST.get('login')
        try:
            admin = Labi.objects.get(login=login)
            request.session['pracownik'] = admin.id
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
            if admin.jednostka.id == '1':
                return redirect('abi_index')
            return redirect('admin_index')
        elif pracownik:
            return redirect('user_index')
        else:
            messages.error(request, 'Błąd logowania')
            return redirect('index')
    return render(request, 'auth_ex/index.html')
