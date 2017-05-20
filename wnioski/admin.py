from django.contrib import admin
from .models import (
    Uprawnienia,
    Jednostki_Organizacyjne,
    Typy_Obiektow_Chronionych,
    Obiekty_Chronione,
    Rodzaje_Pracownikow,
    Pracownicy,
    Wnioski,
    Statusy,
    Historie_Wnioskow,
    Wnioski_Obiekty_Chronione_Uprawnienia,
    Pracownicy_Obiekty_Chronione_Uprawnienia
)


admin.site.register(Uprawnienia)
admin.site.register(Jednostki_Organizacyjne)
admin.site.register(Typy_Obiektow_Chronionych)
admin.site.register(Obiekty_Chronione)
admin.site.register(Rodzaje_Pracownikow)
admin.site.register(Pracownicy)
admin.site.register(Wnioski)
admin.site.register(Statusy)
admin.site.register(Historie_Wnioskow)
admin.site.register(Wnioski_Obiekty_Chronione_Uprawnienia)
admin.site.register(Pracownicy_Obiekty_Chronione_Uprawnienia)
