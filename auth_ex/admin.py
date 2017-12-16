from django.contrib import admin
from .models import (
    Pracownik,
    RodzajPracownika,
    JednOrg,
    Labi,
)

admin.site.register(RodzajPracownika)
admin.site.register(Pracownik)
admin.site.register(JednOrg)
admin.site.register(Labi)
