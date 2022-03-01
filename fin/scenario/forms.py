from django import forms

class PlayForm(forms.Form):
    post = forms.CharField()