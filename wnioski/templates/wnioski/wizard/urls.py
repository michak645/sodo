from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^admin_index$', views.admin_index, name='admin_index'),

    url(r'^wnioski/$', views.wnioski, name='ldap_wniosek_list'),
    url(r'^wniosek/(?P<pk>\d+)/$', views.wniosek_detail, name='ldap_wniosek_detail'),

    url(r'^pracownicy/$', views.PracownikListView.as_view(), name='labi_pracownik_list'),
    url(r'^pracownik/create/$', views.PracownikCreate.as_view(), name='labi_pracownik_create'),
    url(r'^pracownik_rodzaj/create/$', views.RodzajPracownikaCreate.as_view(), name='labi_rodzaj_pracownik_create'),
    url(r'^pracownik/(?P<pk>[\w-]+)/$', views.PracownikDetailView.as_view(), name='labi_pracownik_detail'),

    url(r'^obiekty/$', views.ObiektListView.as_view(), name='labi_obiekt_list'),
    url(r'^obiekt/(?P<pk>\d+)/$', views.ObiektDetailView.as_view(), name='labi_obiekt_detail'),
    url(r'^obiekt/create/$', views.ObiektCreate.as_view(), name='labi_obiekt_create'),
    url(r'^obiekt_typ/create/$', views.ObiektTypCreate.as_view(), name='labi_obiekt_typ_create'),

    url(r'^jednostki/$', views.JednostkaListView.as_view(), name='labi_jednostka_list'),
    url(r'^jednostka/(?P<pk>\d+)/$', views.JednostkaDetailView.as_view(), name='labi_jednostka_detail'),
    url(r'^jednostka/create/$', views.JednostkaCreate.as_view(), name='labi_jednostka_create'),
]
