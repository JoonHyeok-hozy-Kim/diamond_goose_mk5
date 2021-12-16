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
