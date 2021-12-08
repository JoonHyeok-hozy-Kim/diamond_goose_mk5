from django.core.validators import MinValueValidator
from django.db import models
from django import utils

from equityapp.models import Equity

TRANSACTION_TYPE_CHOICES = (
    ('BUY', '매수'),
    ('SELL', '매도'),
    ('DIVIDEND', '배당금'),
    ('SPLIT', '액면분할'),
)

class MinValueFloat(models.FloatField):
    def __init__(self, min_value=None, *args, **kwargs):
        self.min_value = min_value
        super(MinValueFloat, self).__init__(*args, **kwargs)

    def formfield(self, **kwargs):
        defaults = {'min_value': self.min_value}
        defaults.update(kwargs)
        return super(MinValueFloat, self).formfield(**defaults)

class EquityTransaction(models.Model):
    equity = models.ForeignKey(Equity, on_delete=models.CASCADE, related_name='transaction', null=False)

    transaction_type = models.CharField(max_length=20, choices=TRANSACTION_TYPE_CHOICES, null=False)
    quantity = MinValueFloat(min_value=0.0, null=False)

    price = MinValueFloat(min_value=0.0, default=0, null=False)
    transaction_fee = models.FloatField(default=0)
    transaction_tax = models.FloatField(default=0)
    transaction_date = models.DateTimeField(default=utils.timezone.now, null=False)
    note = models.CharField(max_length=20, default=' -', null=True)

    split_flag = models.BooleanField(default=False)

    creation_date = models.DateTimeField(auto_now=True)
    last_update_date = models.DateTimeField(auto_now_add=True)



