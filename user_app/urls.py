from django.conf.urls import url
from user_app import views

urlpatterns = [
    url(r'^user_index', views.user_index, name='user_index'),
    url(r'^user_objects_available', views.user_objects_available, name='user_objects_available'),

    url(r'^user_objects_list', views.obiekt_list, name='user_objects_list'),
    url(r'^user_obiekt/(?P<pk>\d+)/$', views.ObiektDetailView.as_view(), name='user_obiekt_detail'),
    url(r'^user_jednostki/$', views.jednostka_list, name='user_jednostka_list'),
    url(r'^user_jednostka/(?P<pk>\d+)/$', views.JednostkaDetailView.as_view(), name='user_jednostka_detail'),

    url(r'^user_app_accepted', views.user_app_accepted, name='user_app_accepted'),
    url(r'^user_app_rejected', views.user_app_rejected, name='user_app_rejected'),
    url(r'^user_app_detail/(?P<pk>\d+)/$', views.user_app_detail, name='user_app_detail'),

    url(r'^user_profile/$', views.user_profile, name='user_profile'),
    url(r'^user_profile/change_password/step1$', views.change_password_1, name='user_change_password_1'),
    url(r'^user_profile/change_password/step2$', views.change_password_2, name='user_change_password_2'),

    url(r'^admin_panel/$', views.admin_panel, name='admin_panel'),
    url(r'^admin_panel/(?P<pk>\d+)/$', views.admin_panel_detail, name='admin_panel_detail'),

    url(r'^wizard/step_one', views.step_one, name='step_one'),
    url(r'^wizard/step_two', views.step_two, name='step_two'),
    url(r'^wizard/step_three', views.step_three, name='step_three'),
    url(r'^wizard/step_four', views.step_four, name='step_four'),


    url(r'^logout', views.logout, name='logout'),
]