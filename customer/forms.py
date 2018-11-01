from django import forms
from home import choices


class DepositForm(forms.Form):
    account_number = forms.CharField(max_length=100)  # ,disabled=True)
    amount = forms.IntegerField(initial=0)


class WithdrawForm(forms.Form):
    account_number = forms.CharField(max_length=100)  # ,disabled=True)
    amount = forms.IntegerField(initial=0)


class TransferForm(forms.Form):
    account_number = forms.IntegerField()  # ,disabled=True)
    amount = forms.IntegerField(initial=0)
    account_to = forms.IntegerField()


class DetailsForm(forms.Form):
    initial_balance = forms.IntegerField()
