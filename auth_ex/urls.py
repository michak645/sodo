from django.conf.urls import url
from .views import (
    index,
    auth_view,
    logout_view
)


urlpatterns = [
    url(r'^$', index, name='index'),
    url(r'^auth', auth_view, name='auth_view'),
    url(r'^logout', logout_view, name='logout_view'),
]
