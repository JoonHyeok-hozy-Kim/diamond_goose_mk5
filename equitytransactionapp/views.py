import csv
import datetime
import os

from django.contrib.auth.decorators import login_required
from django.core.files.storage import FileSystemStorage
from django.conf import settings
import pandas as pd

# Create your views here.
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse, reverse_lazy
from django.utils.timezone import make_aware
from django.views.generic import CreateView, ListView, DeleteView
from django.views.generic.edit import FormMixin

from equityapp.models import Equity
from equitytransactionapp.forms import EquityTransactionCreationForm
from equitytransactionapp.models import EquityTransaction
from portfolioapp.models import Portfolio


class EquityTransactionCreateView(CreateView):
    model = EquityTransaction
    form_class = EquityTransactionCreationForm
    template_name = 'equitytransactionapp/create.html'

    def form_valid(self, form):
        temp_transaction = form.save(commit=False)
        my_portfolio_scalar_query = Portfolio.objects.filter(owner=self.request.user).values()
        for my_portfolio in my_portfolio_scalar_query:
            target_portfolio_pk = my_portfolio['id']
        target_asset_pk = self.request.POST['asset_pk']
        temp_transaction.equity = Equity.objects.get(asset=target_asset_pk, portfolio=target_portfolio_pk)
        temp_transaction.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('assetmasterapp:detail',kwargs={'pk':self.object.equity.asset.pk})


class EquityTransactionListView(ListView):
    model = EquityTransaction
    context_object_name = 'equity_transaction_list'
    template_name = 'equitytransactionapp/list.html'


class EquityTransactionDeleteView(DeleteView):
    model = EquityTransaction
    context_object_name = 'target_equity_transaction'
    template_name = 'equitytransactionapp/delete.html'

    def get_success_url(self):
        return reverse('assetmasterapp:detail',kwargs={'pk':self.object.equity.asset.pk})


def import_csv(request):
    asset_pk = request.POST['asset_pk']
    my_portfolio_scalar_query = Portfolio.objects.filter(owner=request.user).values()
    for my_portfolio in my_portfolio_scalar_query:
        target_portfolio_pk = my_portfolio['id']

    try:
        if request.method == 'POST' and request.FILES['transaction_file']:

            transaction_file = request.FILES['transaction_file']
            save_dir = os.path.join(settings.MEDIA_ROOT, 'equity_transaction_csv')
            fs = FileSystemStorage(location=save_dir)
            file_name = fs.save(transaction_file.name, transaction_file)
            new_dir = 'equity_transaction_csv/' + file_name

            uploaded_file_url = fs.url(new_dir)
            excel_file = uploaded_file_url
            excel_transaction_data = pd.read_csv("."+excel_file, encoding='utf-8')
            db_frame = excel_transaction_data

            for db_frame in db_frame.itertuples():

                # transaction_date input data make_aware
                try:
                    naive_datetime = datetime.datetime.strptime(db_frame.transaction_date, "%Y-%m-%d %H:%M:%S")
                except Exception as datetime_format_exception1:
                    print('datetime_format_exception1 : ', datetime_format_exception1)
                    try:
                        naive_datetime = datetime.datetime.strptime(db_frame.transaction_date, "%Y-%m-%d %H:%M")
                    except Exception as datetime_format_exception2:
                        print('datetime_format_exception2 : ', datetime_format_exception2)
                        exit()

                aware_datetime = make_aware(naive_datetime)

                # import_transaction_data = [
                #     str(db_frame.transaction_type),
                #     str(db_frame.quantity),
                #     str(db_frame.price),
                #     str(db_frame.transaction_fee),
                #     str(db_frame.transaction_tax),
                #     str(aware_datetime),
                #     str(db_frame.note),
                # ]
                # print(','.join(import_transaction_data))

                obj = EquityTransaction.objects.create(
                    equity=Equity.objects.get(asset=asset_pk, portfolio=target_portfolio_pk),
                    transaction_type=db_frame.transaction_type,
                    quantity=db_frame.quantity,
                    price=db_frame.price,
                    transaction_fee=db_frame.transaction_fee,
                    transaction_tax=db_frame.transaction_tax,
                    transaction_date=aware_datetime,
                    note=db_frame.note
                )

                obj.save()

            return HttpResponseRedirect(reverse('assetmasterapp:detail', kwargs={'pk':asset_pk}))
    except Exception as identifier:
        print(identifier)

    return reverse('assetmasterapp:detail', kwargs={'pk':asset_pk})


def export_csv_template(request):
    asset_pk = request.POST['asset_pk']

    if request.method == 'POST':
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="transaction_csv_template.csv"'
        writer = csv.writer(response)
        # Column Insert
        writer.writerow([
            'transaction_type',
            'quantity',
            'price',
            'transaction_fee',
            'transaction_tax',
            'transaction_date',
            'note',
        ])
        # Sample Line Insert
        writer.writerow([
            'BUY',
            '1',
            '100',
            '1',
            '2',
            '1993-04-27 04:00:00',
            'Sample Format',
        ])

        return response

    return reverse('assetmasterapp:detail', kwargs={'pk': asset_pk})
