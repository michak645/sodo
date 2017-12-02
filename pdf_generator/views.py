from io import BytesIO
from django.template.loader import get_template
from django.http import HttpResponse
from django.views.generic import View

from xhtml2pdf import pisa


def render_to_pdf(template_src, context_dict={}):
    template = get_template(template_src)
    html = template.render(context_dict)
    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), result)
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type='application/pdf')
    return None


class GeneratePdf(View):
    def get(self, request, *args, **kwargs):
        data = {
              'today': 2010,
              'amount': 39.99,
             'customer_name': 'Cooper Mann',
             'order_id': 1233434,
        }
        pdf = render_to_pdf('PDF_wnioski/wniosek_v1.html', data)
        return HttpResponse(pdf, content_type='application/pdf')