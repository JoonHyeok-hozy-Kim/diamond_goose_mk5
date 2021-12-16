from django.forms import widgets, ModelForm
from pensionapp.models import Pension, PensionTransaction, PENSION_TRANSACTION_TYPES


class PensionCreationForm(ModelForm):
    class Meta:
        model = Pension
        fields = ['pension_type', 'risk_ratio_force_flag']


class PensionTransactionCreationForm(ModelForm):
    class Meta:
        model = PensionTransaction
        fields = ['transaction_type', 'amount', 'transaction_date']

        widgets = {
            'transaction_date': widgets.DateTimeInput(attrs={'type':'date'}),
        }