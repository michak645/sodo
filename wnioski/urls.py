from django.conf.urls import url

from . import views

urlpatterns = [

    # main page
    url(r'^$', views.login, name='loggedin'),

    # views
    url(r'^list/', views.list, name='list'),
    url(r'^obiekty/', views.obiekty, name='obiekty'),
    url(r'^pracownicy/', views.pracownicy, name='pracownicy'),
    url(r'^wnioski/', views.wnioski, name='wnioski'),
    url(r'^user_view/(?P<user_id>\d+)/', views.user_view, name='user_view'),
    url(r'^obj_view/(?P<obj_id>\d+)/', views.obj_view, name='obj_view'),
    url(r'^wniosek_view/(?P<wniosek_id>\d+)/', views.wniosek_view,
        name='wniosek_view'),

    # edit
    url(r'^user_edit/(?P<user_id>\d+)/', views.user_edit, name='user_edit'),

    # search
    url(r'^search/', views.search, name='search'),

    # user
    url(r'^acc/login', views.login, name='login'),
    url(r'^acc/authentication', views.authentication, name='authentication'),
    url(r'^acc/logout', views.logout, name='logout'),
    url(r'^acc/invalid', views.invalid, name='invalid'),
    url(r'^user_account/', views.user_account, name='user_account'),

    # create apps
    url(r'^create_app', views.create_app, name='create_app'),
    url(r'^create_user', views.create_user, name='create_user'),
    url(r'^create_obj', views.create_obj, name='create_obj'),

    # LDAP
    url(r'^ldap/login', views.ldap_login, name='ldap_login'),
    url(r'^ldap/main', views.ldap_main, name='ldap_main'),
    url(r'^ldap/auth', views.ldap_auth, name='ldap_auth'),
    url(r'^ldap/obj_list', views.obj_list, name='obj_list'),
    url(r'^ldap/logout', views.ldap_logout, name='ldap_logout'),
    url(r'^ldap/wniosek_view_ldap/(?P<wniosek_id>\d+)',
        views.wniosek_view_ldap, name='wniosek_view_ldap')
]
