from django import forms

from auth_ex.models import Pracownik


class PracownikForm(forms.ModelForm):
    class Meta:
        model = Pracownik
        fields = [
            'imie', 'nazwisko', 'numer_ax', 'email',
            'jedn_org', 'rodzaj', 'aktywny', 'data_zat']
        widgets = {
            'email': forms.EmailInput(),
        }
