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
    typ = ''

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
                typ = 'pracownik'
                request.session['pracownik'] = pracownik.pk
            except Pracownik.DoesNotExist:
                typ = ''
                messages.error(request, 'Błędne dane logowania')
            if pracownik:
                try:
                    labi = Labi.objects.get(login=pracownik)
                    if labi.jednostka.pk == '1':
                        typ = 'abi'
                    else:
                        typ = 'labi'
                    request.session['pracownik'] = labi.pk
                except Labi.DoesNotExist:
                    pass

                if typ == 'abi':
                    return redirect('abi_index')
                elif typ == 'labi':
                    return redirect('admin_index')
                elif typ == 'pracownik':
                    return redirect('user_index')
        else:
            messages.error(request, 'Błąd logowania')
    return render(request, 'auth_ex/index.html')
