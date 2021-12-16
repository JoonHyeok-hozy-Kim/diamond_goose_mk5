from django.forms import ModelForm

from pensionapp.models import Pension


class PensionCreationForm(ModelForm):
    class Meta:
        model = Pension
        fields = ['pension_type', 'risk_ratio_force_flag']