from django.forms import ModelForm
from .models import Wniosek, Pracownik, Obiekt
from django import forms


class WniosekForm(ModelForm):
    class Meta:
        model = Wniosek
        fields = ('typ', 'data_zlo', 'prac_sklada', 'prac_dot', 'obiekt')


class SearchForm(forms.Form):
    username = forms.CharField()


class PracownikForm(ModelForm):
    class Meta:
        model = Pracownik
        fields = (
            'imie', 'nazwisko', 'email', 'data_zatr', 'szkolenie',
            'rodzaj', 'jedn_org', 'login'
        )


class ObiektForm(ModelForm):
    class Meta:
        model = Obiekt
        fields = (
            'nazwa', 'typ', 'jedn_org', 'opis'
        )
