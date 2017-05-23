from django.forms import ModelForm
from .models import Pracownik, Wniosek
from django import forms


class PracownikForm(ModelForm):
    class Meta:
        model = Pracownik
        fields = ('imie', 'nazwisko', 'email', 'data_zatr', 'szkolenie', 'rodzaj', 'jedn_org', 'login', 'haslo')


class WniosekForm(ModelForm):
    class Meta:
        model = Wniosek
        fields = ('typ', 'data_zlo', 'prac_sklada', 'prac_dot', 'obiekt')


class SearchForm(forms.Form):
    username = forms.CharField()
