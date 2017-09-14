from django.contrib import admin
from .models import (
    Uprawnienia,
    JednOrg,
    TypObiektu,
    Obiekt,
    RodzajPracownika,
    Pracownik,
    Wniosek,
    Historia,
    WniosekTyp
)


admin.site.register(Uprawnienia)
admin.site.register(JednOrg)
admin.site.register(TypObiektu)
admin.site.register(Obiekt)
admin.site.register(RodzajPracownika)
admin.site.register(Pracownik)
admin.site.register(Wniosek)
admin.site.register(Historia)
admin.site.register(WniosekTyp)
