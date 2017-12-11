from django.conf.urls import url
from .views import (
    workspace,
    index)


urlpatterns = [
    url(r'^$', index, name='index'),
    url(r'^workspace/', workspace, name='workspace'),
]
