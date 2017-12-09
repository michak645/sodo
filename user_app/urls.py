from django.conf.urls import url
from user_app.views import user_index, user_objects, user_add_app, user_app_accepted, user_app_rejected, \
    user_profile

urlpatterns = [
    url(r'^user_index', user_index, name='user_index'),
    url(r'^user_objects', user_objects, name='user_objects'),
    url(r'^user_add_app', user_add_app, name='user_add_app'),
    url(r'^user_app_accepted', user_app_accepted, name='user_app_accepted'),
    url(r'^user_app_rejected', user_app_rejected, name='user_app_rejected'),
    url(r'^user_profile', user_profile, name='user_profile'),
]
