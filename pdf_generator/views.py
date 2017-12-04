from io import BytesIO
from django.template.loader import get_template
from django.http import HttpResponse
from django.views.generic import *
from xhtml2pdf import pisa
from .models import *
import datetime

def render_to_pdf(template_src, context_dict={}):
    template = get_template(template_src)
    html = template.render(context_dict)
    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode('utf-8')), result)
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type='application/pdf')
    return None


class GenerateRaportPdf(View):
    def get(self,*args, **kwargs):
        wniosek = Wniosek.objects.get(id=kwargs.pop('pk'))
        historia = Historia.objects.filter(wniosek_id=1).order_by('-data')
        print(historia)

        data = {
            'id' : wniosek.pk,
            'pracownik' : wniosek.pracownik,
            'typ' : wniosek.typ,
            'obiekt' : wniosek.obiekt,
            'datazlozenia' : wniosek.data,
            'datawygenerowania' : datetime.datetime.now(),
            'historia' : historia

        }
        pdf = render_to_pdf('PDF_wnioski/wniosek_v1.html', data)
        return HttpResponse(pdf, content_type='application/pdf')

class GenerateWniosekPdf(View):
    def get(self,*args, **kwargs):
        wniosek = Wniosek.objects.get(id=kwargs.pop('pk'))
        historia = Historia.objects.filter(wniosek_id=1).order_by('-data')
        print(historia)

        data = {
            'id' : wniosek.pk,
            'pracownik' : wniosek.pracownik,
            'typ' : wniosek.typ,
            'obiekt' : wniosek.obiekt,
            'datazlozenia' : wniosek.data,
            'datawygenerowania' : datetime.datetime.now(),

        }
        pdf = render_to_pdf('PDF_wnioski/wniosek_v2.html', data)
        return HttpResponse(pdf, content_type='application/pdf')