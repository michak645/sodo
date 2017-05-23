from django.contrib import admin
from .models import (
    Uprawnienia,
    JednOrg,
    TypObiektu,
    Obiekt,
    RodzajPracownika,
    Pracownik,
    Wniosek,
    Status,
    Historia
)


admin.site.register(Uprawnienia)
admin.site.register(JednOrg)
admin.site.register(TypObiektu)
admin.site.register(Obiekt)
admin.site.register(RodzajPracownika)
admin.site.register(Pracownik)
admin.site.register(Wniosek)
admin.site.register(Status)
admin.site.register(Historia)
