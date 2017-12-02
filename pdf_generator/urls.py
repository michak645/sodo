from django.conf.urls import url
from . import views
from .views import (
    GeneratePdf
)

urlpatterns = [
   url(r'^generatepdf/$', GeneratePdf.as_view(), name='generate_pdf'),
]