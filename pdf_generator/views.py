from io import BytesIO
from django.template.loader import get_template
from django.http import HttpResponse
from django.views.generic import *
from xhtml2pdf import pisa
from .models import *
import datetime
from django.conf import settings
from django.http import HttpResponse
from django.template.loader import render_to_string
import weasyprint

def gen_app_pdf(request,pk):
    wniosek = Wniosek.objects.get(pk=pk)
    pracownik = Pracownik.objects.get(pk=wniosek.pracownik.pk)
    html = render_to_string('PDF_wnioski/wniosek_v1.html', {'wniosek': wniosek , 'pracownik': pracownik})
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'filename="wniosek.pdf"'.format(wniosek)
    weasyprint.HTML(string=html).write_pdf(response)
    return response

def gen_app_raport_pdf(request,pk):
    wniosek = Wniosek.objects.get(pk=pk)
    pracownik = Pracownik.objects.get(pk=wniosek.pracownik.pk)
    historia = Historia.objects.filter(wniosek=pk)
    html = render_to_string('PDF_wnioski/wniosek_v2.html', {'wniosek': wniosek , 'pracownik': pracownik, 'historia': historia})
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'filename="wniosek.pdf"'.format(wniosek)
    weasyprint.HTML(string=html).write_pdf(response)
    return response

