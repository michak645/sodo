from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^admin_index$', views.admin_index, name='admin_index'),

    url(r'^wnioski/', views.wnioski, name='wnioski'),
    url(r'^wniosek/(?P<pk>\d+)/', views.wniosek_detail, name='wniosek_detail'),

    url(r'^pracownicy/', views.PracownikListView.as_view(), name='labi_pracownik_list'),
    url(r'^pracownik/(?P<pk>[\w-]+)/', views.PracownikDetailView.as_view(), name='labi_pracownik_detail'),

    url(r'^obiekty/', views.ObiektListView.as_view(), name='labi_obiekt_list'),
    url(r'^obiekt/(?P<pk>\d+)/', views.ObiektDetailView.as_view(), name='labi_obiekt_detail'),

    url(r'^typy_obiektow/', views.typy_obiektow, name='typy_obiektow'),
    url(r'^jednostki/', views.jednostki, name='jednostki'),
    url(r'^typ_obiektu_view/(?P<typ_obiektu_id>\d+)/',
        views.typ_obiektu_view, name='typ_obiektu_view'),
    url(r'^jednostka_view/(?P<pk>\d+)/',
        views.jednostka_view, name='jednostka_view'),

    # edit
    url(r'^obj_edit/(?P<obj_id>\d+)/', views.obj_edit, name='obj_edit'),
    url(r'^app_edit/(?P<app_id>\d+)/', views.app_edit, name='app_edit'),
    url(r'^typ_obiektu_edit/(?P<typ_obiektu_id>\d+)/',
        views.typ_obiektu_edit, name='typ_obiektu_edit'),
    url(r'^jednostka_edit/(?P<jednostka_id>\d+)/',
        views.jednostka_edit, name='jednostka_edit'),

    # user
    url(r'^user_account/', views.user_account, name='user_account'),

    # create apps
    url(r'^create_app', views.create_app, name='create_app'),
    url(r'^create_user', views.create_user, name='create_user'),
    url(r'^create_obj', views.create_obj, name='create_obj'),
    url(r'^create_type', views.create_type, name='create_type'),
    url(r'^create_unit', views.create_unit, name='create_unit'),
]
