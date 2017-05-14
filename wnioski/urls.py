from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^add/', views.add, name='add'),
    url(r'^list/', views.list, name='list'),

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
