from django import forms
from .models import Portal


class PortalForm(forms.ModelForm):
    
    class Meta:
        model = Portal
        fields = ('name', 'user')
        widgets = {'name': forms.HiddenInput(), 'user': forms.HiddenInput()}