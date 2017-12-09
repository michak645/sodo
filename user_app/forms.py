from django import forms

from wnioski.models import Wniosek


class AddApplicationForm(forms.ModelForm):
    class Meta:
        model = Wniosek
        fields = ['pracownik', 'typ', 'obiekt']
        widgets = {
            'pracownik': forms.HiddenInput(),
        }
