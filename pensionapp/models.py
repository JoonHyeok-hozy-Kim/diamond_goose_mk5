from django.contrib.auth.models import User
from django.db import models

# Create your models here.
from dashboardapp.models import Dashboard
from portfolioapp.models import Portfolio

PENSION_TYPES = (
    ('퇴직연금', '퇴직연금'),
    ('연금저축', '연금저축'),
    ('IRP', 'IRP'),
)


class Pension(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='pension')
    dashboard = models.ForeignKey(Dashboard, on_delete=models.CASCADE, related_name='pension')

    pension_type = models.CharField(max_length=30, choices=PENSION_TYPES, null=False)
    total_paid_amount = models.FloatField(default=0, null=False)
    total_current_value = models.FloatField(default=0, null=False)
    total_profit_amount = models.FloatField(default=0, null=False)
    rate_of_return = models.FloatField(default=0, null=False)

    risk_ratio_force_flag = models.BooleanField(default=False, null=False)
    risk_ratio = models.FloatField(default=0.7, null=True)
    current_risk_asset_ratio = models.FloatField(default=0, null=True)


    def calculate_total_paid_amount(self):
        pension_transaction_query = self.pension_transaction.all()
        new_total_paid_amount = 0
        for transaction in pension_transaction_query:
            if transaction.transaction_type == 'PAY':
                new_total_paid_amount += transaction.amount
            else:
                new_total_paid_amount -= transaction.amount

        pension = Pension.objects.filter(pk=self.pk)
        pension.update(total_paid_amount=new_total_paid_amount)


PENSION_TRANSACTION_TYPES = (
    ('PAY', '납입'),
    ('RECEIVE', '수령'),
)


class PensionTransaction(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='pension_transaction')
    pension = models.ForeignKey(Pension, on_delete=models.CASCADE, related_name='pension_transaction')

    transaction_type = models.CharField(max_length=20, choices=PENSION_TRANSACTION_TYPES, null=False)
    amount = models.FloatField(default=0, null=False)

    transaction_date = models.DateTimeField(null=False)
    creation_date = models.DateTimeField(auto_now=True)
    last_update_date = models.DateTimeField(auto_now_add=True)


