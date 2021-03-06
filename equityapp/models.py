from django.contrib.auth.models import User
from django.db import models

# Create your models here.
from django.db.models import Q

from assetmasterapp.models import Asset
from portfolioapp.models import Portfolio


class Equity(models.Model):
    asset = models.ForeignKey(Asset, on_delete=models.CASCADE, related_name='equity', null=False)
    portfolio = models.ForeignKey(Portfolio, on_delete=models.CASCADE, related_name='equity', null=False)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='equity', null=False)

    quantity = models.FloatField(default=0, null=False)
    total_amount = models.FloatField(default=0, null=False)
    average_purchase_price_mv = models.FloatField(default=0, null=False)
    average_purchase_price_fifo = models.FloatField(default=0, null=False)

    rate_of_return_mv = models.FloatField(default=0, null=False)
    rate_of_return_fifo = models.FloatField(default=0, null=False)

    creation_date = models.DateTimeField(auto_now=True)
    last_update_date = models.DateTimeField(auto_now_add=True)

    def update_quantity_amount_prices(self):
        query = Q(transaction_type='BUY')
        query.add(Q(transaction_type='SELL'),Q.OR)
        query.add(Q(quantity__gt=0),Q.AND)
        query.add(Q(split_flag=False),Q.AND)

        transaction_data_set = self.transaction.filter(query).values()
        equity = Equity.objects.filter(pk=self.pk)

        # quantity
        final_quantity = 0
        for transaction_data in transaction_data_set:
            if transaction_data['transaction_type'] == 'BUY':
                final_quantity += transaction_data['quantity']
            else:
                final_quantity -= transaction_data['quantity']

        equity.update(quantity=final_quantity)

        # amount
        current_price = self.asset.current_price
        equity.update(total_amount=final_quantity*current_price)

        # average_purchase_price_mv
        temp_qty = 0
        temp_amt = 0
        average_purchase_price_mv = 0
        for transaction_data in transaction_data_set:
            if transaction_data['transaction_type'] == 'BUY':
                temp_qty += transaction_data['quantity']
                temp_amt += transaction_data['quantity'] * transaction_data['price']
            else:
                temp_price = temp_amt/temp_qty
                temp_qty -= transaction_data['quantity']
                temp_amt = temp_qty * temp_price

        if temp_qty < 0: average_purchase_price_mv = -999
        elif temp_qty > 0: average_purchase_price_mv = temp_amt/temp_qty
        equity.update(average_purchase_price_mv=average_purchase_price_mv)

        # average_purchase_price_fifo
        transaction_amount_list = []
        temp_qty = 0
        temp_amt = 0
        for transaction_data in transaction_data_set:
            if transaction_data['transaction_type'] == 'BUY':
                for i in range(int(transaction_data['quantity'])):
                    transaction_amount_list.append(transaction_data['price'])
            else:
                for i in range(int(transaction_data['quantity'])):
                    transaction_amount_list.pop(0)

        for transaction_amount in transaction_amount_list:
            temp_qty += 1
            temp_amt += transaction_amount

        if temp_qty > 0: average_purchase_price_fifo = temp_amt/temp_qty
        else: average_purchase_price_fifo = 0
        equity.update(average_purchase_price_fifo=average_purchase_price_fifo)

        return {
            'quantity': final_quantity,
            'total_amount': final_quantity*current_price,
            'average_purchase_price_mv': average_purchase_price_mv,
            'average_purchase_price_fifo': average_purchase_price_fifo,
        }

    def update_rate_of_returns(self):
        equity = Equity.objects.filter(pk=self.pk)

        rate_of_return_mv = 0
        if self.average_purchase_price_mv > 0:
            rate_of_return_mv = (self.asset.current_price - self.average_purchase_price_mv)/self.average_purchase_price_mv
        equity.update(rate_of_return_mv=rate_of_return_mv)

        rate_of_return_fifo = 0
        if self.average_purchase_price_fifo > 0:
            rate_of_return_fifo = (self.asset.current_price - self.average_purchase_price_fifo)/self.average_purchase_price_fifo
        equity.update(rate_of_return_fifo=rate_of_return_fifo)

        return{
            'rate_of_return_mv': rate_of_return_mv,
            'rate_of_return_fifo': rate_of_return_fifo,
        }
