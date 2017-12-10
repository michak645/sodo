from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^gen_app_pdf/(?P<pk>\d+)/$', views.gen_app_pdf, name='gen_app_pdf'),
    url(r'^gen_app_raport_pdf/(?P<pk>\d+)/$', views.gen_app_raport_pdf, name='gen_app_raport_pdf')

]
