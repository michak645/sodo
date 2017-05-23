from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.login, name='login'),
    url(r'^add/', views.add, name='add'),
    url(r'^list/', views.list, name='list'),
    url(r'^search/', views.search, name='search'),
    url(r'^user_view/(?P<user_id>\d+)/', views.user_view, name='user_view'),
    url(r'^user_account/', views.user_account, name='user_account'),

    url(r'^acc/login', views.login, name='login'),
    url(r'^acc/authentication', views.authentication, name='authentication'),
    url(r'^acc/logout', views.logout, name='logout'),
    url(r'^acc/loggedin', views.loggedin, name='loggedin'),
    url(r'^acc/invalid', views.invalid, name='invalid'),

    url(r'^acc/create_user$', views.create_user, name='create_user'),
    url(r'^acc/create_user_succ$', views.create_user_succ,
        name='create_user_succ'),
    url(r'^acc/create_user_error', views.create_user_error,
        name='create_user_error')

]
