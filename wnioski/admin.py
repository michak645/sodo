from django.contrib import admin
from .models import (
    TypObiektu,
    Obiekt,
    Wniosek,
    Historia,
)


admin.site.register(TypObiektu)
admin.site.register(Obiekt)
admin.site.register(Wniosek)
admin.site.register(Historia)

