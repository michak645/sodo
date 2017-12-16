from django import forms

from auth_ex.models import Pracownik, JednOrg


class PracownikForm(forms.ModelForm):
    class Meta:
        model = Pracownik
        fields = [
            'imie', 'nazwisko', 'numer_ax', 'email',
            'jedn_org', 'rodzaj']
        widgets = {
            'email': forms.EmailInput(),
        }


class JednostkaForm(forms.ModelForm):
    class Meta:
        model = JednOrg
        fields = ['id', 'parent', 'czy_labi', 'nazwa']
