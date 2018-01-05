from django.conf.urls import url
from user_app.views import (
    user_index, user_objects_available, user_add_app,
    user_app_accepted, user_app_rejected, user_profile, user_objects_list,
    user_app_detail, user_app_add_object, step_one, step_two, step_three,
    step_four,
)

urlpatterns = [
    url(r'^user_index', user_index, name='user_index'),
    url(r'^user_objects_available', user_objects_available,
        name='user_objects_available'),
    url(r'^user_objects_list', user_objects_list, name='user_objects_list'),
    url(r'^user_add_app', user_add_app, name='user_add_app'),
    url(r'^user_app_accepted', user_app_accepted, name='user_app_accepted'),
    url(r'^user_app_rejected', user_app_rejected, name='user_app_rejected'),
    url(r'^user_profile', user_profile, name='user_profile'),
    url(r'^user_app_detail/(?P<pk>\d+)/$', user_app_detail,
        name='user_app_detail'),
    url(r'^user_app_add_object/(?P<pk>\d+)/$', user_app_add_object,
        name='user_app_add_object'),

    url(r'^wizard/step_one', step_one, name='step_one'),
    url(r'^wizard/step_two', step_two, name='step_two'),
    url(r'^wizard/step_three', step_three, name='step_three'),
    url(r'^wizard/step_four', step_four, name='step_four'),
]
