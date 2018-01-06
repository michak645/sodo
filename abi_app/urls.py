from django.conf.urls import url
from abi_app import views

urlpatterns = [
    url(r'^abi_index', views.abi_index, name='abi_index'),
]
