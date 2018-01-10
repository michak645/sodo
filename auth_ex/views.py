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


def authenticate(request):
    pracownik = request.session['pracownik']
    typ = ''
    try:
        pracownik = int(pracownik)
    except (ValueError, TypeError):
        pass
    try:
        labi = Labi.objects.get(id=pracownik)
        typ = 'labi'
        if labi.jednostka.pk == '1':
            typ = 'abi'
    except Labi.DoesNotExist:
        typ = ''

    try:
        Pracownik.objects.get(login=pracownik)
        typ = 'pracownik'
    except Pracownik.DoesNotExist:
        typ = ''
    return typ


def index(request):
    prac = False
    labi = False
    abi = False

    typ = authenticate(request)
    if typ == 'pracownik':
        return redirect('user_index')
    if typ == 'labi':
        return redirect('admin_index')
    if typ == 'abi':
        return redirect('abi_index')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        if username and password:
            try:
                pracownik = Pracownik.objects.get(
                    login=username,
                    password=password,
                    czy_user=True,
                )
                prac = True
                request.session['pracownik'] = pracownik.pk
            except Pracownik.DoesNotExist:
                pracownik = None
                prac = False
                messages.error(request, 'Błędne dane logowania')

            if pracownik:
                try:
                    pracownik = Labi.objects.get(login=pracownik)
                    labi = True
                    request.session['pracownik'] = pracownik.pk
                except Labi.DoesNotExist:
                    labi = False
                if labi:
                    if pracownik.jednostka == '1':
                        abi = True
                        request.session['pracownik'] = pracownik.pk
                    else:
                        abi = False
                if abi:
                    return redirect('abi_index')
                elif labi:
                    return redirect('admin_index')
                elif prac:
                    return redirect('user_index')
        else:
            messages.error(request, 'Błąd logowania')
    return render(request, 'auth_ex/index.html')
