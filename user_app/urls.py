from django.conf.urls import url
from user_app.views import user_index, user_applications, user_add_app

urlpatterns = [
    url(r'^user_index', user_index, name='user_index'),
    url(r'^user_applications', user_applications, name='user_applications'),
    url(r'^user_add_app', user_add_app, name='user_add_app'),
]
