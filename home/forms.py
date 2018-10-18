from django import forms
from home import choices


class DetailsForm(forms.Form):
    first_name = forms.CharField(max_length=100)
    last_name = forms.CharField(max_length=100)
    email_address = forms.EmailField()
    choices = forms.ChoiceField(label='Account Type',choices = choices.GROUP)

