from django.conf.urls import url
from abi_app import views

urlpatterns = [
    url(r'^abi_index$', views.abi_index, name='abi_index'),

    url(r'^abi/wniosek_list', views.wniosek_list, name='wniosek_list'),
    url(r'^abi/wniosek_detail/(?P<pk>\d+)/$', views.wniosek_detail,
        name='abi_wniosek_detail'),

    url(r'^abi/pracownicy/$', views.pracownik_list, name='abi_pracownik_list'),
    url(r'^abi/pracownik/create/$', views.PracownikCreate.as_view(), name='abi_pracownik_create'),
    url(r'^abi/pracownik_rodzaj/create/$', views.RodzajPracownikaCreate.as_view(), name='abi_rodzaj_pracownik_create'),
    url(r'^abi/pracownik/(?P<pk>[\w-]+)/$', views.pracownik_detail, name='abi_pracownik_detail'),

    url(r'^abi/obiekty/$', views.obiekt_list, name='abi_obiekt_list'),
    url(r'^abi/obiekt/(?P<pk>\d+)/$', views.obiekt_detail, name='abi_obiekt_detail'),
    url(r'^abi/obiekt/create/$', views.ObiektCreate.as_view(), name='abi_obiekt_create'),
    url(r'^abi/obiekt_typ/create/$', views.ObiektTypCreate.as_view(), name='abi_obiekt_typ_create'),
    url(r'^abi/as/create/$', views.as_create, name='abi_as_create'),

    url(r'^abi/jednostki/$', views.jednostka_list, name='abi_jednostka_list'),
    url(r'^abi/jednostka/(?P<pk>\d+)/$', views.JednostkaDetailView.as_view(), name='abi_jednostka_detail'),
    url(r'^abi/jednostka/create/$', views.JednostkaCreate.as_view(), name='abi_jednostka_create'),

    url(r'^abi/wizard/step_one', views.step_one, name='abi_step_one'),
    url(r'^abi/wizard/step_two', views.step_two, name='abi_step_two'),
    url(r'^abi/wizard/step_three', views.step_three, name='abi_step_three'),
    url(r'^abi/wizard/step_four', views.step_four, name='abi_step_four'),

]
