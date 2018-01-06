from django.conf.urls import url
from auth_ex import views


urlpatterns = [
    url(r'^$', views.index, name='index'),
]
