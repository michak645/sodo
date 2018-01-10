from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^admin_index$', views.admin_index, name='admin_index'),

    url(r'^wnioski/$', views.wnioski, name='labi_wniosek_list'),
    url(r'^wniosek/(?P<pk>\d+)/$', views.wniosek_detail, name='labi_wniosek_detail'),

    url(r'^pracownicy/$', views.pracownik_list, name='labi_pracownik_list'),
    url(r'^pracownik/create/$', views.PracownikCreate.as_view(), name='labi_pracownik_create'),
    url(r'^pracownik_rodzaj/create/$', views.RodzajPracownikaCreate.as_view(), name='labi_rodzaj_pracownik_create'),
    url(r'^pracownik/(?P<pk>[\w-]+)/$', views.PracownikDetailView.as_view(), name='labi_pracownik_detail'),

    url(r'^obiekty/$', views.obiekt_list, name='labi_obiekt_list'),
    url(r'^obiekt/(?P<pk>\d+)/$', views.obiekt_detail, name='labi_obiekt_detail'),
    url(r'^obiekt/create/$', views.ObiektCreate.as_view(), name='labi_obiekt_create'),
    url(r'^obiekt_typ/create/$', views.ObiektTypCreate.as_view(), name='labi_obiekt_typ_create'),

    url(r'^as/create/$', views.as_create, name='labi_as_create'),

    url(r'^jednostki/$', views.jednostka_list, name='labi_jednostka_list'),
    url(r'^jednostka/(?P<pk>\d+)/$', views.JednostkaDetailView.as_view(), name='labi_jednostka_detail'),
    url(r'^jednostka/create/$', views.JednostkaCreate.as_view(), name='labi_jednostka_create'),

    url(r'^labi/wizard/step_one', views.step_one, name='labi_step_one'),
    url(r'^labi/wizard/step_two', views.step_two, name='labi_step_two'),
    url(r'^labi/wizard/step_three', views.step_three, name='labi_step_three'),
    url(r'^labi/wizard/step_four', views.step_four, name='labi_step_four'),
]
