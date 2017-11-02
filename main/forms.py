from django import forms

class MainForms(forms.Form):
    title = forms.CharField(max_length=120, required=True)
    url_from = forms.CharField(required=True, label='From')
    url_to = forms.CharField(required=True, label='To')
