from django.contrib import admin
from .models import (
    Pracownik,
    RodzajPracownika,
    JednOrg,
    Labi,
    Drzewo
)

admin.site.register(RodzajPracownika)
admin.site.register(Pracownik)
admin.site.register(JednOrg)
admin.site.register(Labi)
admin.site.register(Drzewo)
