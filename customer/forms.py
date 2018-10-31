from django import forms
from home import choices


class DetailsForm(forms.Form):
    initial_balance = forms.IntegerField()