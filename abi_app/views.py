from django.http import HttpResponseRedirect
from django.shortcuts import render

from auth_ex.models import Labi
from wnioski.models import (
    Wniosek,
    Historia,
    PracownicyObiektyUprawnienia,
)


def abi_index(request):
    pracownik = Labi.objects.get(id=request.session['pracownik'])

    if request.method == 'POST':
        wnioski = Wniosek.objects.all().order_by('data')
        data_nowe = request.POST.get('data-nowe')
        data_stare = request.POST.get('data-stare')
        if data_nowe:
            wnioski = Wniosek.objects.order_by('-data')
        elif data_stare:
            wnioski = Wniosek.objects.order_by('data')

        if request.POST.get('zatwierdz'):
            checked = request.POST.getlist('decyzja')

            for pk in checked:
                w = Wniosek.objects.get(id=pk)
                Historia.objects.create(
                    wniosek_id=pk,
                    status='3',
                )
                if w.typ == '1':
                    for obiekt in w.obiekty.all():
                        for uprawnienia in w.uprawnienia:
                            for pracownik in w.pracownicy.all():
                                PracownicyObiektyUprawnienia.objects \
                                    .get_or_create(
                                        login=pracownik,
                                        id_obiektu=obiekt,
                                        uprawnienia=uprawnienia
                                    )
                elif w.typ == '2':
                    try:
                        for obiekt in w.obiekty.all():
                            for uprawnienia in w.uprawnienia:
                                for pracownik in w.pracownicy.all():
                                    PracownicyObiektyUprawnienia.objects.get(
                                        login=pracownik,
                                        id_obiektu=obiekt,
                                        uprawnienia=uprawnienia
                                    ).delete()
                    except PracownicyObiektyUprawnienia.DoesNotExist:
                        pass
        elif request.POST.get('odrzuc'):
            Historia.objects.create(
                wniosek_id=pk,
                status='5',
            )
            historia = Historia.objects.filter(wniosek=pk)
            return HttpResponseRedirect('/abi_index')
    else:
        wnioski = Wniosek.objects.all().order_by('data')

    to_approve = []
    for wniosek in wnioski:
        historia = Historia.objects.filter(
            wniosek=wniosek.id,
        ).order_by('-data')[0]
        if historia.status == '2':
            to_approve.append(historia)

    context = {
        'wnioski': to_approve,
        'pracownik': pracownik,
    }
    return render(request, 'abi_app/abi_index.html', context)
