from django.conf.urls import url, include
from django.contrib import admin

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^', include('wnioski.urls')),
    url(r'^', include('auth_ex.urls')),
    url(r'^', include('pdf_generator.urls')),
    url(r'^', include('user_app.urls')),
    url(r'^', include('abi_app.urls')),
]
