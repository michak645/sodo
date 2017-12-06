from django.conf.urls import url
from .views import (
    index,
    auth_view,
    logout_view,
    UserListView,
    UserDetailView,
    UserDeleteView,
    UserUpdateView,
    workspace,
)


urlpatterns = [
    url(r'^$', index, name='index'),
    url(r'^auth', auth_view, name='auth_view'),
    url(r'^logout', logout_view, name='logout_view'),
    url(r'^user_list', UserListView.as_view(), name='user_list'),
    url(r'^user_detail/(?P<pk>[0-9]+)/', UserDetailView.as_view(), name='user_detail'),
    url(r'^user_update/(?P<pk>[0-9]+)/', UserUpdateView, name='user_update'),
    url(r'^user/delete/(?P<pk>[0-9]+)/', UserDeleteView.as_view(), name='user_delete'),
    url(r'^workspace/', workspace, name='workspace'),
]
