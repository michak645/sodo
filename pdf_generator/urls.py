from django.conf.urls import url
from . import views
from .views import (
    GenerateRaportPdf,
    GenerateWniosekPdf
)

urlpatterns = [
    url(r'^wniosekraport/(?P<pk>\d+)/', GenerateRaportPdf.as_view(), name='generate_pdf'),
    url(r'^wniosekpdf/(?P<pk>\d+)/', GenerateWniosekPdf.as_view(), name='generate_pdf')

]