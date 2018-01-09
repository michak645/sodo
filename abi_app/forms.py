from django import forms


class PracownikAktywnyForm(forms.Form):
    czy_aktywny = forms.BooleanField()
