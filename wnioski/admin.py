from django.contrib import admin
from .models import (
    TypObiektu,
    Obiekt,
    Wniosek,
    Historia,
    PracownicyObiektyUprawnienia,
    AdministratorObiektu,
    ZatwierdzonePrzezAS,
)


admin.site.register(TypObiektu)
admin.site.register(Obiekt)
admin.site.register(Wniosek)
admin.site.register(Historia)
admin.site.register(PracownicyObiektyUprawnienia)
admin.site.register(AdministratorObiektu)
admin.site.register(ZatwierdzonePrzezAS)
