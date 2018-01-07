from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^gen_app_pdf/(?P<pk>\d+)/$', views.gen_app_pdf, name='gen_app_pdf'),
    url(r'^gen_app_raport_pdf/(?P<pk>\d+)/$', views.gen_app_raport_pdf, name='gen_app_raport_pdf'),
    url(r'^gen_objs_raport_csv/$', views.gen_objs_raport_csv, name='gen_objs_raport_csv'),
    url(r'^gen_apps_raport_csv/$', views.gen_apps_raport_csv, name='gen_apps_raport_csv'),
    url(r'^gen_appupr_raport_csv/$', views.gen_appupr_raport_csv, name='gen_appupr_raport_csv'),
    url(r'^gen_appobj_raport_csv/$', views.gen_appobj_raport_csv, name='gen_appobj_raport_csv'),
    url(r'^gen_appprac_raport_csv/$', views.gen_appprac_raport_csv, name='gen_appprac_raport_csv'),
    url(r'^gen_hist_raport_csv/$', views.gen_hist_raport_csv, name='gen_hist_raport_csv'),

]
