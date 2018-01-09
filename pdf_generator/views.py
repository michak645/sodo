from .models import *
from django.http import HttpResponse
from django.template.loader import render_to_string
import weasyprint
import csv
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from django.conf import settings
import weasyprint
from io import BytesIO
from django.http import HttpResponseRedirect


def gen_app_pdf(request,pk):
    wniosek = Wniosek.objects.get(pk=pk)
    pracownik = Pracownik.objects.get(pk=wniosek.pracownik.pk)
    html = render_to_string('PDF_wnioski/wniosek_pdf_wzor.html', {'wniosek': wniosek , 'pracownik': pracownik})
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'filename="wniosek.pdf"'.format(wniosek)
    weasyprint.HTML(string=html).write_pdf(response)
    return response


def mail_app_pdf(request,pk):
    wniosek = Wniosek.objects.get(pk=pk)
    pracownik = Pracownik.objects.get(pk=wniosek.pracownik.pk)
    subject = 'złożyłeś wniosek w systemie SODO'
    message = 'Złożyłeś wniosek w systemie SODO. Przesyłamy go w załączniku.'
    email = EmailMessage(subject, message, 'sodo.uam.test@gmail.com', ['kamil.trb@gmail.com'])
    html = render_to_string('PDF_wnioski/wniosek_pdf_wzor.html', {'wniosek': wniosek , 'pracownik': pracownik})
    out = BytesIO()
    weasyprint.HTML(string=html).write_pdf(out)
    email.attach('order.pdf', out.getvalue(), 'application/pdf')
    email.send()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER')) #nie wiem co tu dac, zalezy tez od uzycia


def gen_app_raport_pdf(request,pk):
    wniosek = Wniosek.objects.get(pk=pk)
    pracownik = Pracownik.objects.get(pk=wniosek.pracownik.pk)
    historia = Historia.objects.filter(wniosek=pk)
    html = render_to_string('PDF_wnioski/wniosek_rap_pdf_wzor.html', {'wniosek': wniosek , 'pracownik': pracownik, 'historia': historia})
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'filename="wniosek.pdf"'.format(wniosek)
    weasyprint.HTML(string=html).write_pdf(response)
    return response


def gen_objs_raport_csv(request):
    obiekty = Obiekt.objects.all()
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="raport_obiekty.csv"'
    writer = csv.writer(response)
    writer.writerow(['id', 'nazwa_obiektu', 'typ_id', 'typ', 'jedn_org_id', 'jedn_org', 'opis'])
    for o in obiekty:
        writer.writerow([o.pk, o.nazwa, o.typ.id, o.typ.nazwa, o.jedn_org.id, o.jedn_org.nazwa, o.opis,])
    return response


def gen_apps_raport_csv(request):
    wnioski = Wniosek.objects.all()
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="raport_wnioski.csv"'
    writer = csv.writer(response)
    writer.writerow(['id', 'data', 'typ_id', 'typ', 'pracownik_sklad', 'komentarz'])
    for w in wnioski:
        writer.writerow([w.pk, w.data, w.typ, w.get_typ_display(), w.pracownik.login, w.komentarz])
    return response


def gen_appupr_raport_csv(request):
    wnioski = Wniosek.objects.all()
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="raport_wnioskiuprawnienia.csv"'
    writer = csv.writer(response)
    writer.writerow(['id_wniosku', 'id_upr'])
    for w in wnioski:
        for u in w.uprawnienia:
            writer.writerow([w.pk, u])
    return response


def gen_appobj_raport_csv(request):
    wnioski = Wniosek.objects.all()
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="raport_wnioskiobiekty.csv"'
    writer = csv.writer(response)
    writer.writerow(['id_wniosku', 'id_obj'])
    for w in wnioski:
        for o in w.obiekty.all():
            writer.writerow([w.pk, o.pk])
    return response


def gen_appprac_raport_csv(request):
    wnioski = Wniosek.objects.all()
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="raport_wnioskipracownicy.csv"'
    writer = csv.writer(response)
    writer.writerow(['id_wniosku', 'id_prac'])
    for w in wnioski:
        for p in w.pracownicy.all():
            writer.writerow([w.pk, p.pk])
    return response


def gen_hist_raport_csv(request):
    historie = Historia.objects.all()
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="raport_historia.csv"'
    writer = csv.writer(response)
    writer.writerow(['id_hist', 'id_wniosku', 'data', 'status_id', 'status', 'id_prac'])
    for h in historie:
        if h.pracownik:
            writer.writerow([h.pk, h.wniosek.pk, h.data, h.status, h.get_status(), h.pracownik.pk])
        else:
            writer.writerow([h.pk, h.wniosek.pk, h.data, h.status, h.get_status(), 'none'])
    return response