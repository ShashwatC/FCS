from django import forms
from django.core.exceptions import ValidationError

from home import choices


class DepositForm(forms.Form):
    def clean_amount(self):
        amount = self.cleaned_data['amount']
        if amount < 0:
            raise ValidationError("Amount must be positive")
        return amount

    account_number = forms.CharField(max_length=100)  # ,disabled=True)
    amount = forms.IntegerField(initial=0)


class WithdrawForm(forms.Form):
    def clean_amount(self):
        amount = self.cleaned_data['amount']
        if amount < 0:
            raise ValidationError("Amount must be positive")
        return amount

    account_number = forms.CharField(max_length=100)  # ,disabled=True)
    amount = forms.IntegerField(initial=0)


class TransferForm(forms.Form):
    def clean_amount(self):
        amount = self.cleaned_data['amount']
        if amount < 0:
            raise ValidationError("Amount must be positive")
        return amount

    account_number = forms.IntegerField()  # ,disabled=True)
    amount = forms.IntegerField(initial=0)
    account_to = forms.IntegerField()


class DetailsForm(forms.Form):
    initial_balance = forms.IntegerField()

class ProfileForm(forms.Form):
    first_name = forms.CharField(max_length=100)
    last_name = forms.CharField(max_length=100)
    email_address = forms.EmailField()
    mobile_number = forms.CharField(max_length=100)
