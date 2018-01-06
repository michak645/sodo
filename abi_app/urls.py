from django.conf.urls import url
from abi_app import views

urlpatterns = [
    url(r'^abi_index', views.abi_index, name='abi_index'),

    url(r'^abi/wniosek_list', views.wniosek_list, name='wniosek_list'),
    url(r'^abi/wniosek_detail/(?P<pk>\d+)/$', views.wniosek_detail,
        name='abi_wniosek_detail'),

    url(r'^abi/obiekt_list', views.obiekt_list, name='obiekt_list'),

    url(r'^abi/wizard/step_one', views.step_one, name='abi_step_one'),
    url(r'^abi/wizard/step_two', views.step_two, name='abi_step_two'),
    url(r'^abi/wizard/step_three', views.step_three, name='abi_step_three'),
    url(r'^abi/wizard/step_four', views.step_four, name='abi_step_four'),

]
