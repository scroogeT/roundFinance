from django import forms
from django.contrib.auth.forms import UserCreationForm

from .models import transactions

class transactionsForm(forms.ModelForm):
    class Meta:
        model = transactions
        fields = ('amount','interestRate','descriptionOfUse')
