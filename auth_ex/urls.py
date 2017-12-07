from django.conf.urls import url
from .views import (
    workspace,
    index,
    auth_view)


urlpatterns = [
    url(r'^$', index, name='index'),
    url(r'^auth_view', auth_view, name='auth_view'),
    url(r'^workspace/', workspace, name='workspace'),
]
