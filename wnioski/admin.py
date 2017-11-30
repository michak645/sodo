from django.contrib import admin
from .models import (
    Uprawnienia,
    JednOrg,
    TypObiektu,
    Obiekt,
    Wniosek,
    Historia,
    WniosekTyp,
)


admin.site.register(Uprawnienia)
admin.site.register(JednOrg)
admin.site.register(TypObiektu)
admin.site.register(Obiekt)
admin.site.register(Wniosek)
admin.site.register(Historia)
admin.site.register(WniosekTyp)
