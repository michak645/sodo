# -*- coding: utf-8 -*-
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
import weasyprint
from io import BytesIO

from auth_ex.views import find_labi
from .models import (
    Wniosek,
    Obiekt,
    Historia,
    TypObiektu,
    ZatwierdzonePrzezAS,
    PracownicyObiektyUprawnienia,
    AdministratorObiektu,
)
from .forms import (
    ObiektFiltrowanieForm,
    ObiektyFiltrowanieForm,
    WniosekFiltrowanieForm,
    PracownicyFiltrowanieForm,
    JednostkiFiltrowanieForm,
)
from auth_ex.models import (
    JednOrg,
    Pracownik,
    Labi,
    RodzajPracownika,
)
from user_app.models import Cart
from user_app.forms import WizardUprawnienia


def authenticate(request):
    try:
        prac = request.session['pracownik']
        labi = Labi.objects.get(pk=prac)
        if labi.jednostka.pk == '1':
            return None
        else:
            return labi
    except:
        return None


def admin_index(request):
    pracownik = authenticate(request)
    if not pracownik:
        messages.warning(
            request,
            'Musisz się najpierw zalogować jako LABI'
        )
        return redirect('index')

    wnioski = Wniosek.objects.all().order_by('-data')

    if request.method == 'POST':
        wnioski = Wniosek.objects.all().order_by('data')
        if request.POST.get('data-nowe'):
            wnioski = Wniosek.objects.order_by('-data')
        elif request.POST.get('data-stare'):
            wnioski = Wniosek.objects.order_by('data')

        if request.POST.get('zatwierdz'):
            checked = request.POST.getlist('decyzja')
            for pk in checked:
                Historia.objects.create(
                    wniosek_id=pk,
                    status='2',
                    pracownik=pracownik.login,
                )
        elif request.POST.get('odrzuc'):
            checked = request.POST.getlist('decyzja')
            for pk in checked:
                Historia.objects.create(
                    wniosek_id=pk,
                    status='5',
                    pracownik=pracownik.login,
                )
                ''' zakomentowane bo dlugo robi i nie chce spamowac, zreszta maile pracownikow sa fejkowe
                wniosek_mail = Wniosek.objects.get(pk=pk)
                pracownik_w = Pracownik.objects.get(pk=wniosek_mail.pracownik.pk)
                historia_w = Historia.objects.filter(wniosek=pk)
                subject = 'SODO: odrzucowno wniosek nr '+str(wniosek_mail.pk)+' w systemie'
                message = 'Odrzucono twój wniosek o numerze '+str(wniosek_mail.pk)+'.\n' \
                    'Do wiadomości dołączono raport z historią wniosku.\n' \
                    'Wiadomość wygenerowana automatycznie.'
                send_addr = wniosek_mail.pracownik.email
                email = EmailMessage(subject, message, 'sodo.uam.test@gmail.com', [send_addr])
                html = render_to_string('PDF_wnioski/wniosek_rap_pdf_wzor.html',
                                        {'wniosek': wniosek_mail, 'pracownik': pracownik_w, 'historia': historia_w})
                out = BytesIO()
                weasyprint.HTML(string=html).write_pdf(out)
                email.attach('raport_wniosek'+str(wniosek_mail.pk)+'.pdf', out.getvalue(), 'application/pdf')
                email.send()
                '''
            historia = Historia.objects.filter(wniosek=pk)
            return redirect('admin_index')

    to_approve = []
    for wniosek in wnioski:
        obiekt = wniosek.obiekty.all()[0]
        wniosek_labi = find_labi(obiekt.jedn_org.id)
        if wniosek_labi == pracownik:
            historia = Historia.objects.filter(
                wniosek=wniosek.id,
            ).order_by('-data')[0]
            if historia.status == '1':
                to_approve.append(historia)

    context = {
        'pracownik': pracownik,
        'wnioski': wnioski,
        'to_approve': to_approve,
    }
    return render(request, 'wnioski/homepage/homepage.html', context)


def wnioski(request):
    pracownik = authenticate(request)
    if not pracownik:
        messages.warning(
            request,
            'Musisz się najpierw zalogować jako LABI'
        )
        return redirect('index')

    wnioski = Wniosek.objects.all().order_by('-data')

    if request.method == 'POST':
        form = WniosekFiltrowanieForm(request.POST)
        if form.is_valid():
            if request.POST.get('clear'):
                form = ObiektFiltrowanieForm()
            else:
                obiekt = form.cleaned_data['obiekt']
                if obiekt:
                    wnioski = wnioski.filter(
                        obiekty__nazwa__icontains=obiekt
                    )
                jednostka = form.cleaned_data['jednostka']
                if jednostka:
                    wnioski = wnioski.filter(
                        obiekty__jedn_org__nazwa__icontains=jednostka
                    )
                pracownik = form.cleaned_data['pracownik']
                if pracownik:
                    wnioski = wnioski.filter(
                        pracownik__nazwisko__icontains=pracownik,
                    )
                uprawnienia = form.cleaned_data['uprawnienia']
                if uprawnienia:
                    wnioski = wnioski.filter(
                        uprawnienia__icontains=uprawnienia,
                    )
                if form.cleaned_data['data']:
                    wnioski = wnioski.filter(
                        data__date=form.cleaned_data['data'],
                    )
    else:
        form = WniosekFiltrowanieForm()

    paginator = Paginator(wnioski, 10)
    page = request.GET.get('page')
    try:
        wnioski = paginator.page(page)
    except PageNotAnInteger:
        wnioski = paginator.page(1)
    except EmptyPage:
        wnioski = paginator.page(paginator.num_pages)

    context = {
        'form': form,
        'pracownik': pracownik,
        'wnioski': wnioski,
    }
    return render(request, 'wnioski/wniosek/wniosek_list.html', context)


def wniosek_detail(request, pk):
    pracownik = authenticate(request)
    if not pracownik:
        messages.warning(
            request,
            'Musisz się najpierw zalogować jako LABI'
        )
        return redirect('index')

    template = 'wnioski/wniosek/wniosek_detail.html'
    w = Wniosek.objects.get(id=pk)
    # date = datetime.now()
    if request.method == 'POST':
        if request.POST.get('change') == "Zatwierdź":
            Historia.objects.create(
                wniosek_id=pk,
                status='2',
                pracownik=pracownik.login,
            )
            historia = Historia.objects. \
                filter(wniosek=pk). \
                order_by('-data')

            return HttpResponseRedirect('/admin_index')
        elif request.POST.get('change') == "Odrzuć":
            Historia.objects.create(
                wniosek_id=pk,
                status='5',
                pracownik=pracownik.login,
            )
            ''' zakomentowane bo dlugo robi i nie chce spamowac, zreszta maile pracownikow sa fejkowe
            wniosek_mail = Wniosek.objects.get(pk=pk)
            pracownik_w = Pracownik.objects.get(pk=wniosek_mail.pracownik.pk)
            historia_w = Historia.objects.filter(wniosek=pk)
            subject = 'SODO: odrzucowno wniosek nr ' + str(wniosek_mail.pk) + ' w systemie'
            message = 'Odrzucono twój wniosek o numerze ' + str(wniosek_mail.pk) + '.\n' \
                'Do wiadomości dołączono raport z historią wniosku.\n' \
                'Wiadomość wygenerowana automatycznie.'
            send_addr = wniosek_mail.pracownik.email
            email = EmailMessage(subject, message, 'sodo.uam.test@gmail.com', [send_addr])
            html = render_to_string('PDF_wnioski/wniosek_rap_pdf_wzor.html',
                                    {'wniosek': wniosek_mail, 'pracownik': pracownik_w, 'historia': historia_w})
            out = BytesIO()
            weasyprint.HTML(string=html).write_pdf(out)
            email.attach('raport_wniosek' + str(wniosek_mail.pk) + '.pdf', out.getvalue(), 'application/pdf')
            email.send()
            '''
            historia = Historia.objects.filter(wniosek=pk)
            return HttpResponseRedirect('/admin_index')
    else:
        historia = Historia.objects. \
            filter(wniosek=pk). \
            order_by('-data')
        status = historia[0].get_status_display()
        status_int = historia[0].status
        return render(request, template, {
            'wniosek': w,
            'historia': historia,
            'status': status,
            'status_int': status_int,
        })


def pracownik_list(request):
    pracownik = authenticate(request)
    if not pracownik:
        messages.warning(
            request,
            'Musisz się najpierw zalogować jako LABI'
        )
        return redirect('index')

    pracownicy = Pracownik.objects.all().order_by('nazwisko')

    if request.method == 'POST':
        form = PracownicyFiltrowanieForm(request.POST)
        if form.is_valid():
            if request.POST.get('clear'):
                form = ObiektFiltrowanieForm()
            else:
                nazwisko = form.cleaned_data['nazwisko']
                if nazwisko:
                    pracownicy = pracownicy.filter(
                        nazwisko__icontains=nazwisko
                    )
                jednostka = form.cleaned_data['jednostka']
                if jednostka:
                    pracownicy = pracownicy.filter(
                        jedn_org__nazwa__icontains=jednostka
                    )
                numer_ax = form.cleaned_data['numer_ax']
                if numer_ax:
                    pracownicy = pracownicy.filter(
                        numer_ax__icontains=numer_ax,
                    )
                rodzaj = form.cleaned_data['rodzaj']
                if rodzaj:
                    pracownicy = pracownicy.filter(
                        rodzaj__rodzaj__icontains=rodzaj,
                    )
    else:
        form = PracownicyFiltrowanieForm()

    paginator = Paginator(pracownicy, 10)
    page = request.GET.get('page')
    try:
        pracownicy = paginator.page(page)
    except PageNotAnInteger:
        pracownicy = paginator.page(1)
    except EmptyPage:
        pracownicy = paginator.page(paginator.num_pages)

    context = {
        'pracownik': pracownik,
        'pracownicy': pracownicy,
        'form': form,
    }
    return render(request, 'wnioski/pracownik/pracownik_list.html', context)


class PracownikDetailView(DetailView):
    model = Pracownik
    template_name = 'wnioski/pracownik/pracownik_detail.html'
    context_object_name = 'prac'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pracownik = authenticate(self.request)
        context['pracownik'] = pracownik
        wnioski = Wniosek.objects.filter(
            pracownik=self.object.pk).order_by('-data')
        historie = []
        for wniosek in wnioski:
            try:
                hist = Historia.objects.filter(
                    wniosek=wniosek).order_by('-data')[0]
                historie.append(hist)
            except IndexError:
                hist = None
        wnioski_pracownika = []
        for wniosek in wnioski:
            for prac_wniosek in wniosek.pracownicy.all():
                if prac_wniosek.pk == self.object.pk:
                    wnioski_pracownika.append(wniosek)

        paginator = Paginator(historie, 5)
        page = self.request.GET.get('page')
        try:
            historie = paginator.page(page)
        except PageNotAnInteger:
            historie = paginator.page(1)
        except EmptyPage:
            historie = paginator.page(paginator.num_pages)

        obiekty = ZatwierdzonePrzezAS.objects.filter(
            wniosek__in=wnioski_pracownika,
        )

        context['historie'] = historie
        context['obiekty'] = obiekty
        return context

    def get(self, *args, **kwargs):
        pracownik = authenticate(self.request)
        if not pracownik:
            messages.warning(
                self.request,
                'Musisz się najpierw zalogować jako pracownik'
            )
            return redirect('index')
        return super().get(*args, **kwargs)


class PracownikCreate(CreateView):
    model = Pracownik
    fields = ['login', 'imie', 'nazwisko', 'email',
              'rodzaj', 'jedn_org', 'numer_ax']
    template_name = 'wnioski/pracownik/pracownik_create.html'
    success_url = reverse_lazy('labi_pracownik_list')

    def form_valid(self, form):
        messages.success(self.request, 'Pomyślnie dodano pracownika.')
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pracownik = authenticate(self.request)
        context['pracownik'] = pracownik
        return context

    def get(self, *args, **kwargs):
        pracownik = authenticate(self.request)
        if not pracownik:
            messages.warning(
                self.request,
                'Musisz się najpierw zalogować jako pracownik'
            )
            return redirect('index')
        return super().get(*args, **kwargs)


class RodzajPracownikaCreate(CreateView):
    model = RodzajPracownika
    fields = ['rodzaj', ]
    template_name = 'wnioski/pracownik/rodzaj_pracownika_create.html'
    success_url = reverse_lazy('labi_pracownik_list')

    def form_valid(self, form):
        messages.success(self.request, 'Pomyślnie dodano rodzaj pracownika.')
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pracownik = authenticate(self.request)
        context['pracownik'] = pracownik
        return context

    def get(self, *args, **kwargs):
        pracownik = authenticate(self.request)
        if not pracownik:
            messages.warning(
                self.request,
                'Musisz się najpierw zalogować jako pracownik'
            )
            return redirect('index')
        return super().get(*args, **kwargs)


def as_create(request):
    pracownik = authenticate(request)
    if not pracownik:
        messages.warning(
            request,
            'Musisz się najpierw zalogować jako LABI'
        )
        return redirect('index')
    pracownicy = Pracownik.objects.all()
    obiekty_z_as = AdministratorObiektu.objects.values('obiekt')
    obiekty = Obiekt.objects.exclude(id__in=obiekty_z_as)

    obiekt = None
    prac = None

    if request.method == 'POST':
        if request.POST.get('szukaj'):
            if request.POST.get('szukaj_obiektu'):
                obiekty = obiekty.filter(
                    nazwa__icontains=request.POST.get('szukaj_obiektu')
                )
            if request.POST.get('szukaj_pracownika'):
                pracownicy = pracownicy.filter(
                    nazwisko__icontains=request.POST.get('szukaj_pracownika')
                )
            if request.POST.get('wybrany_prac'):
                prac = Pracownik.objects.get(
                    pk=request.POST.get('wybrany_prac'),
                )
            if request.POST.get('wybrany_obiekt'):
                obiekt = Obiekt.objects.get(
                    id=request.POST.get('wybrany_obiekt'),
                )
        if request.POST.get('add_obiekt'):
            obiekt = Obiekt.objects.get(
                id=request.POST.get('obiekt'),
            )
            if request.POST.get('wybrany_prac'):
                prac = Pracownik.objects.get(
                    pk=request.POST.get('wybrany_prac'),
                )
        if request.POST.get('add_prac'):
            prac = Pracownik.objects.get(
                pk=request.POST.get('prac'),
            )
            if request.POST.get('wybrany_obiekt'):
                obiekt = Obiekt.objects.get(
                    id=request.POST.get('wybrany_obiekt'),
                )
        if request.POST.get('zapisz'):
            obiekt = request.POST.get('wybrany_obiekt')
            prac = request.POST.get('wybrany_prac')
            if obiekt and prac:
                obiekt = Obiekt.objects.get(
                    id=obiekt,
                )
                prac = Pracownik.objects.get(
                    pk=prac,
                )
                AdministratorObiektu.objects.create(
                    pracownik=prac,
                    obiekt=obiekt,
                )
                messages.success(
                    request,
                    'Pomyslnie dodano administratora systemu'
                )
                return redirect('admin_index')
            else:
                messages.error(request, 'błąd')

    paginator = Paginator(pracownicy, 10)
    page = request.GET.get('page')
    try:
        pracownicy = paginator.page(page)
    except PageNotAnInteger:
        pracownicy = paginator.page(1)
    except EmptyPage:
        pracownicy = paginator.page(paginator.num_pages)

    obiekty_labi = []
    for o in obiekty:
        if (get_labi(o.jedn_org.id) == pracownik):
            obiekty_labi.append(o)

    paginator = Paginator(obiekty_labi, 10)
    page = request.GET.get('page')
    try:
        obiekty_labi = paginator.page(page)
    except PageNotAnInteger:
        obiekty_labi = paginator.page(1)
    except EmptyPage:
        obiekty_labi = paginator.page(paginator.num_pages)

    context = {
        'pracownicy': pracownicy,
        'obiekty': obiekty_labi,
        'obiekt': obiekt,
        'prac': prac,
    }
    return render(request, 'wnioski/as/as_create.html', context)


def obiekt_list(request):
    pracownik = authenticate(request)
    if not pracownik:
        messages.warning(
            request,
            'Musisz się najpierw zalogować jako LABI'
        )
        return redirect('index')

    obiekty = Obiekt.objects.all().order_by('nazwa')

    if request.method == 'POST':
        form = ObiektyFiltrowanieForm(request.POST)
        if form.is_valid():
            if request.POST.get('clear'):
                form = ObiektFiltrowanieForm()
            else:
                if form.cleaned_data['nazwa']:
                    obiekty = obiekty.filter(
                        nazwa__icontains=form.cleaned_data['nazwa']
                    )
                if form.cleaned_data['jednostka']:
                    jedn = form.cleaned_data['jednostka']
                    obiekty = obiekty.filter(
                        jedn_org__nazwa__icontains=jedn
                    )
                if form.cleaned_data['typ']:
                    obiekty = obiekty.filter(
                        typ__nazwa__icontains=form.cleaned_data['typ'],
                    )
    else:
        form = ObiektyFiltrowanieForm()

    paginator = Paginator(obiekty, 10)
    page = request.GET.get('page')
    try:
        obiekty = paginator.page(page)
    except PageNotAnInteger:
        obiekty = paginator.page(1)
    except EmptyPage:
        obiekty = paginator.page(paginator.num_pages)

    context = {
        'pracownik': pracownik,
        'obiekty': obiekty,
        'form': form,
    }
    return render(request, 'wnioski/obiekt/obiekt_list.html', context)


def obiekt_detail(request, pk):
    pracownik = authenticate(request)
    if not pracownik:
        messages.warning(
            request,
            'Musisz się najpierw zalogować jako LABI'
        )
        return redirect('index')
    obiekt = Obiekt.objects.get(pk=pk)
    try:
        as_obiekt = AdministratorObiektu.objects.get(obiekt=obiekt)
    except AdministratorObiektu.DoesNotExist:
        as_obiekt = None
    pou = PracownicyObiektyUprawnienia.objects.filter(
        id_obiektu=obiekt
    )
    pracownicy = Pracownik.objects.filter(
        login__in=pou.values('login')
    )
    jednostki = JednOrg.objects.filter(
        id__in=pracownicy.values('jedn_org')
    )
    if request.method == 'POST':
        form = ObiektFiltrowanieForm(request.POST)
        if form.is_valid():
            if request.POST.get('clear'):
                form = ObiektFiltrowanieForm()
            else:
                if form.cleaned_data['pracownik']:
                    pracownicy = pracownicy.filter(
                        nazwisko__icontains=form.cleaned_data['pracownik']
                    )
                if form.cleaned_data['jednostka']:
                    jednostki = jednostki.filter(
                        nazwa__icontains=form.cleaned_data['jednostka']
                    )
                if form.cleaned_data['uprawnienia']:
                    pou = pou.filter(
                        uprawnienia__in=form.cleaned_data['uprawnienia'],
                    )
    else:
        form = ObiektFiltrowanieForm()

    context = {
        'pracownik': pracownik,
        'obiekt': obiekt,
        'pou': pou,
        'form': form,
        'pracownicy': pracownicy,
        'jednostki': jednostki,
        'as_obiekt': as_obiekt,
    }
    return render(request, 'wnioski/obiekt/obiekt_detail.html', context)


class ObiektCreate(CreateView):
    model = Obiekt
    fields = ['nazwa', 'typ', 'jedn_org', 'opis']
    template_name = 'wnioski/obiekt/obiekt_create.html'
    success_url = reverse_lazy('labi_obiekt_list')

    def form_valid(self, form):
        messages.success(self.request, 'Pomyślnie dodano obiekt.')
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pracownik = authenticate(self.request)
        context['pracownik'] = pracownik
        return context

    def get(self, *args, **kwargs):
        pracownik = authenticate(self.request)
        if not pracownik:
            messages.warning(
                self.request,
                'Musisz się najpierw zalogować jako pracownik'
            )
            return redirect('index')
        return super().get(*args, **kwargs)


class ObiektTypCreate(CreateView):
    model = TypObiektu
    fields = ['nazwa', ]
    template_name = 'wnioski/obiekt/obiekt_typ_create.html'
    success_url = reverse_lazy('labi_obiekt_list')

    def form_valid(self, form):
        messages.success(self.request, 'Pomyślnie dodano typ obiektu.')
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pracownik = authenticate(self.request)
        context['pracownik'] = pracownik
        return context

    def get(self, *args, **kwargs):
        pracownik = authenticate(self.request)
        if not pracownik:
            messages.warning(
                self.request,
                'Musisz się najpierw zalogować jako pracownik'
            )
            return redirect('index')
        return super().get(*args, **kwargs)


def jednostka_list(request):
    pracownik = authenticate(request)
    if not pracownik:
        messages.warning(
            request,
            'Musisz się najpierw zalogować jako LABI'
        )
        return redirect('index')
    jednostki = JednOrg.objects.all().order_by('nazwa')

    if request.method == 'POST':
        form = JednostkiFiltrowanieForm(request.POST)
        if form.is_valid():
            if request.POST.get('clear'):
                form = ObiektFiltrowanieForm()
            else:
                nazwa = form.cleaned_data['nazwa']
                if nazwa:
                    jednostki = jednostki.filter(
                        nazwa__icontains=nazwa
                    )
                czy_labi = form.cleaned_data['czy_labi']
                if czy_labi:
                    jednostki = jednostki.filter(
                        czy_labi=czy_labi
                    )
                parent = form.cleaned_data['parent']
                if parent:
                    jednostki = jednostki.filter(
                        parent__nazwa__icontains=parent,
                    )
    else:
        form = JednostkiFiltrowanieForm()

    paginator = Paginator(jednostki, 10)
    page = request.GET.get('page')
    try:
        jednostki = paginator.page(page)
    except PageNotAnInteger:
        jednostki = paginator.page(1)
    except EmptyPage:
        jednostki = paginator.page(paginator.num_pages)

    context = {
        'pracownik': pracownik,
        'jednostki': jednostki,
        'form': form,
    }
    return render(request, 'wnioski/jednostka/jednostka_list.html', context)


class JednostkaDetailView(DetailView):
    model = JednOrg
    template_name = 'wnioski/jednostka/jednostka_detail.html'
    context_object_name = 'jednostka'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        pracownik = authenticate(self.request)
        context['pracownik'] = pracownik
        if self.object.czy_labi:
            labi = Labi.objects.get(jednostka=self.object.id)
        else:
            labi = None
        context['labi'] = labi
        return context

    def get(self, *args, **kwargs):
        pracownik = authenticate(self.request)
        if not pracownik:
            messages.warning(
                self.request,
                'Musisz się najpierw zalogować jako pracownik'
            )
            return redirect('index')
        return super().get(*args, **kwargs)


class JednostkaCreate(CreateView):
    model = JednOrg
    fields = ['nazwa', 'parent', 'czy_labi']
    template_name = 'wnioski/jednostka/jednostka_create.html'
    success_url = reverse_lazy('labi_jednostka_list')

    def form_valid(self, form):
        messages.success(self.request, 'Pomyślnie dodano jednostkę.')
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pracownik = authenticate(self.request)
        context['pracownik'] = pracownik
        return context

    def get(self, *args, **kwargs):
        pracownik = authenticate(self.request)
        if not pracownik:
            messages.warning(
                self.request,
                'Musisz się najpierw zalogować jako pracownik'
            )
            return redirect('index')
        return super().get(*args, **kwargs)


def step_one(request):
    pracownik = authenticate(request)
    if not pracownik:
        messages.warning(
            request,
            'Musisz się najpierw zalogować jako LABI'
        )
        return redirect('index')
    cart, created = Cart.objects.get_or_create(id=pracownik.pk)
    obj_list = None
    jednostka = None
    jednostki = JednOrg.objects.all().order_by('nazwa')
    wszedzie = False

    if request.method == 'POST':
        obj = request.POST.get('obj')

        szukaj_jednostki = request.POST.get('szukaj-jednostki')
        if szukaj_jednostki:
            jednostki = JednOrg.objects.filter(
                nazwa__icontains=szukaj_jednostki
            )
        szukaj_obiektu = request.POST.get('szukaj-obiektu')
        if szukaj_obiektu:
            jednostka = request.POST.get('wybrana-jednostka')
            if request.POST.get('szukaj_wszedzie'):
                obj_list = Obiekt.objects.filter(
                    nazwa__icontains=szukaj_obiektu,
                    czy_aktywny=True
                )
                wszedzie = True
            else:
                if jednostka:
                    jednostka = JednOrg.objects.get(id=jednostka)
                else:
                    messages.warning(request, 'Najpierw wybierz jednostkę')
                obj_list = Obiekt.objects.filter(
                    jedn_org=jednostka,
                    nazwa__icontains=szukaj_obiektu,
                    czy_aktywny=True
                )
                wszedzie = False

        if request.POST.get('clear'):
            cart.obiekty.clear()

        if request.POST.get('delete'):
            cart.obiekty.remove(Obiekt.objects.get(id=obj))

        if request.POST.get('add'):
            cart.obiekty.add(Obiekt.objects.get(id=obj))
            jednostka = request.POST.get('jednostka')
            if jednostka:
                obj_list = Obiekt.objects.filter(
                    jedn_org=jednostka,
                    czy_aktywny=True
                )
                jednostka = JednOrg.objects.get(id=jednostka)

        if request.POST.get('show'):
            jednostka = request.POST.get('jednostka')
            obj_list = Obiekt.objects.filter(
                jedn_org=jednostka,
                czy_aktywny=True
            )
            jednostka = JednOrg.objects.get(id=jednostka)

        if request.POST.get('dodaj_wszystkie'):
            jednostka = request.POST.get('wybrana-jednostka')
            if jednostka:
                obj_list = Obiekt.objects.filter(
                    jedn_org=jednostka,
                    czy_aktywny=True
                )
                obiekty = Obiekt.objects.filter(
                    jedn_org=jednostka,
                    czy_aktywny=True
                )
                for obiekt in obiekty:
                    cart.obiekty.add(obiekt)
                obj_list = Obiekt.objects.filter(
                    jedn_org=jednostka,
                    czy_aktywny=True
                )
        if obj_list:
            paginator = Paginator(obj_list, 10)
            page = request.GET.get('page_obiekt')
            try:
                obj_list = paginator.page(page)
            except PageNotAnInteger:
                obj_list = paginator.page(1)
            except EmptyPage:
                obj_list = paginator.page(paginator.num_pages)

    paginator = Paginator(jednostki, 10)
    page = request.GET.get('page')
    try:
        jednostki = paginator.page(page)
    except PageNotAnInteger:
        jednostki = paginator.page(1)
    except EmptyPage:
        jednostki = paginator.page(paginator.num_pages)

    objs_cart = cart.obiekty.all()
    paginator = Paginator(objs_cart, 10)
    page = request.GET.get('page')
    try:
        objs_cart = paginator.page(page)
    except PageNotAnInteger:
        objs_cart = paginator.page(1)
    except EmptyPage:
        objs_cart = paginator.page(paginator.num_pages)

    context = {
        'wybrana_jednostka': jednostka,
        'jednostki': jednostki,
        'obj_list': obj_list,
        'pracownik': pracownik,
        'objs_cart': objs_cart,
        'wszedzie': wszedzie,
    }
    return render(request, 'wnioski/wizard/step_one.html', context)


def step_two(request):
    pracownik = authenticate(request)
    if not pracownik:
        messages.warning(
            request,
            'Musisz się najpierw zalogować jako LABI'
        )
        return redirect('index')
    cart = Cart.objects.get(id=pracownik.pk)
    prac_list = None
    jednostka = None
    jednostki = JednOrg.objects.all().order_by('nazwa')
    wszedzie = False

    if request.method == 'POST':
        prac = request.POST.get('prac')

        szukaj_jednostki = request.POST.get('szukaj-jednostki')
        if szukaj_jednostki:
            jednostki = JednOrg.objects.filter(
                nazwa__icontains=szukaj_jednostki
            )

        szukaj_pracownika = request.POST.get('szukaj-pracownika')
        if szukaj_pracownika:
            jednostka = request.POST.get('wybrana-jednostka')
            if request.POST.get('szukaj_wszedzie'):
                prac_list = Pracownik.objects.filter(
                    nazwisko__icontains=szukaj_pracownika,
                    czy_aktywny=True
                )
                wszedzie = True
            else:
                if jednostka:
                    jednostka = JednOrg.objects.get(id=jednostka)
                else:
                    messages.warning(request, 'Najpierw wybierz jednostkę')
                prac_list = Pracownik.objects.filter(
                    jedn_org=jednostka,
                    nazwisko__icontains=szukaj_pracownika,
                    czy_aktywny=True,
                )
                wszedzie = False

        if request.POST.get('clear'):
            cart.pracownicy.clear()

        if request.POST.get('delete'):
            cart.pracownicy.remove(Pracownik.objects.get(login=prac))

        if request.POST.get('add'):
            cart.pracownicy.add(Pracownik.objects.get(login=prac))
            jednostka = request.POST.get('jednostka')
            if jednostka:
                prac_list = Pracownik.objects.filter(
                    jedn_org=jednostka,
                    czy_aktywny=True,
                )
                jednostka = JednOrg.objects.get(id=jednostka)

        if request.POST.get('show'):
            jednostka = request.POST.get('jednostka')
            prac_list = Pracownik.objects.filter(
                jedn_org=jednostka,
                czy_aktywny=True,
            )
            jednostka = JednOrg.objects.get(id=jednostka)

        if request.POST.get('dodaj_wszystkie'):
            jednostka = request.POST.get('wybrana-jednostka')
            if jednostka:
                prac_list = Pracownik.objects.filter(
                    jedn_org=jednostka,
                    czy_aktywny=True
                )
                pracownicy_temp = Pracownik.objects.filter(
                    jedn_org=jednostka,
                    czy_aktywny=True
                )
                for pracownik in pracownicy_temp:
                    cart.pracownicy.add(pracownik)
                prac_list = Pracownik.objects.filter(
                    jedn_org=jednostka,
                    czy_aktywny=True
                )

        if prac_list:
            paginator = Paginator(prac_list, 10)
            page = request.GET.get('page_obiekt')
            try:
                prac_list = paginator.page(page)
            except PageNotAnInteger:
                prac_list = paginator.page(1)
            except EmptyPage:
                prac_list = paginator.page(paginator.num_pages)

    paginator = Paginator(jednostki, 10)
    page = request.GET.get('page')
    try:
        jednostki = paginator.page(page)
    except PageNotAnInteger:
        jednostki = paginator.page(1)
    except EmptyPage:
        jednostki = paginator.page(paginator.num_pages)

    prac_cart = cart.pracownicy.all()
    paginator = Paginator(prac_cart, 10)
    page = request.GET.get('page')
    try:
        prac_cart = paginator.page(page)
    except PageNotAnInteger:
        prac_cart = paginator.page(1)
    except EmptyPage:
        prac_cart = paginator.page(paginator.num_pages)

    context = {
        'wybrana_jednostka': jednostka,
        'jednostki': jednostki,
        'pracownik': pracownik,
        'prac_list': prac_list,
        'prac_cart': prac_cart,
        'wszedzie': wszedzie,
    }
    return render(request, 'wnioski/wizard/step_two.html', context)


def step_three(request):
    pracownik = authenticate(request)
    if not pracownik:
        messages.warning(
            request,
            'Musisz się najpierw zalogować jako LABI'
        )
        return redirect('index')
    cart = Cart.objects.get(id=pracownik.pk)
    aktualne_uprawnienia = PracownicyObiektyUprawnienia.objects.filter(
        login__in=cart.pracownicy.all(),
        id_obiektu__in=cart.obiekty.all()
    )
    obiekty = {}
    for obiekt in cart.obiekty.all():
        pracownicy = {}
        for pracownik in cart.pracownicy.all():
            pou = PracownicyObiektyUprawnienia.objects.filter(
                login=pracownik,
                id_obiektu=obiekt,
            )
            if pou:
                pracownicy[pracownik] = pou
        obiekty[obiekt] = pracownicy

    if request.method == 'POST':
        form = WizardUprawnienia(request.POST)
        if form.is_valid():
            cart.uprawnienia = form.cleaned_data['uprawnienia']
            cart.typ_wniosku = form.cleaned_data['typ_wniosku']
            cart.save()
            return redirect('labi_step_four')
        else:
            messages.error(request, 'Wypełnij poprawnie formularz')
    else:
        form = WizardUprawnienia()

    pracownicy = cart.pracownicy.all()

    paginator = Paginator(pracownicy, 10)
    page = request.GET.get('page')
    try:
        pracownicy = paginator.page(page)
    except PageNotAnInteger:
        pracownicy = paginator.page(1)
    except EmptyPage:
        pracownicy = paginator.page(paginator.num_pages)

    context = {
        'pracownik': pracownik,
        'pracownicy': pracownicy,
        'cart': cart,
        'aktualne_uprawnienia': aktualne_uprawnienia,
        'form': form,
        'obiekty': obiekty,
    }
    return render(request, 'wnioski/wizard/step_three.html', context)


def get_labi(jedn):
    try:
        jednostka = JednOrg.objects.get(id=jedn)
    except JednOrg.DoesNotExist as e:
        return e
    if jednostka.czy_labi:
        return Labi.objects.get(jednostka=jednostka.id)
    else:
        return get_labi(jednostka.parent.id)


def step_four(request):
    pracownik = authenticate(request)
    if not pracownik:
        messages.warning(
            request,
            'Musisz się najpierw zalogować jako LABI'
        )
        return redirect('index')
    cart = Cart.objects.get(id=pracownik.pk)

    cart_objs = cart.obiekty.all()
    labi_list = []
    for obj in cart_objs:
        if get_labi(obj.jedn_org.id) not in labi_list:
            labi_list.append(get_labi(obj.jedn_org.id))

    wnioski = []
    for labi in labi_list:
        wniosek = {}
        wniosek['labi'] = labi
        wniosek_obiekty = []
        for obj in cart_objs:
            if get_labi(obj.jedn_org.id) == labi:
                wniosek_obiekty.append(obj)
        wniosek['obiekty'] = wniosek_obiekty
        wniosek['pracownicy'] = cart.pracownicy.all()
        wniosek['uprawnienia'] = cart.get_uprawnienia_display()
        wniosek['typ_wniosku'] = cart.get_typ_wniosku_display()
        wnioski.append(wniosek)

    if request.method == 'POST':
        for wniosek in wnioski:
            w = Wniosek.objects.create(
                typ=cart.typ_wniosku,
                pracownik=pracownik.login,
                uprawnienia=cart.uprawnienia,
            )
            for prac_temp in cart.pracownicy.all():
                w.pracownicy.add(prac_temp)
            for obiekt in wniosek['obiekty']:
                w.obiekty.add(obiekt)
            komentarz_id = 'komentarz' + str(wniosek['labi'].id)
            komentarz = request.POST.get(komentarz_id)
            w.komentarz = komentarz
            w.save()
            ''' zakomentowane bo dlugo robi i nie chce spamowac, zreszta maile pracownikow sa fejkowe
            subject = 'SODO: nowy wniosek nr '+str(w.pk)+' w systemie'
            message = 'Złożyłeś nowy wniosek w systemie SODO.\nWniosek otrzymał numer '+str(w.pk)+', ' \
                'został umieszczony w systemie i oczekuje na decyzję Lokalnego Administratora ' \
                'Bezpieczeństwa Informacji.\nDokument w formacie PDF został dołączony do tej wiadomości.\n' \
                'Wiadomość wygenerowana automatycznie.'
            send_addr = w.pracownik.email
            email = EmailMessage(subject, message, 'sodo.uam.test@gmail.com', [send_addr])
            html = render_to_string('PDF_wnioski/wniosek_pdf_wzor.html', {'wniosek': w, 'pracownik': pracownik})
            out = BytesIO()
            weasyprint.HTML(string=html).write_pdf(out)
            email.attach('wniosek'+str(w.pk)+'.pdf', out.getvalue(), 'application/pdf')
            email.send()
            '''
        cart.delete()
        return HttpResponseRedirect('/admin_index')
    context = {
        'wnioski': wnioski,
        'pracownik': pracownik,
        'cart': cart,
    }
    return render(request, 'wnioski/wizard/step_four.html', context)
