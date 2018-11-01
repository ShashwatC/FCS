from django import forms
from home import choices


class DetailsForm(forms.Form):
    first_name = forms.CharField(max_length=100)
    last_name = forms.CharField(max_length=100)
    email_address = forms.EmailField()
    choice = forms.ChoiceField(label='Account Type',choices=choices.GROUP)
    mobile_number = forms.RegexField(regex=r'^\+?1?\d{9,15}$')
    public_key = forms.CharField(max_length=1024,widget=forms.Textarea)
    # private key later maybe
