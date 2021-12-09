import os

from django.shortcuts import render

# Create your views here.
from django.urls import reverse
from django.views.generic import ListView, CreateView, DetailView
from django.views.generic.edit import FormMixin, UpdateView, DeleteView
from django.utils.text import Truncator

from assetmasterapp.forms import AssetCreationForm
from assetmasterapp.models import Asset
from diamond_goose_mk5.settings import MEDIA_ROOT
from equityapp.forms import EquityCreationForm
from equityapp.models import Equity
from equitytransactionapp.forms import EquityTransactionCreationForm
from equitytransactionapp.models import EquityTransaction
from portfolioapp.models import Portfolio


class AssetListView(ListView):
    model = Asset
    context_object_name = 'target_asset_list'
    template_name = 'assetmasterapp/list.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(AssetListView, self).get_context_data(**kwargs)

        query_asset_list = Asset.objects.all().order_by('asset_type','ticker').values()
        for query_asset in query_asset_list:
            query_asset['name'] = Truncator(query_asset['name']).chars(29)
            query_asset['image'] = 'media/'+query_asset['image']

        context.update({'query_asset_list': query_asset_list})

        return context


class AssetCreateView(CreateView):
    model = Asset
    form_class = AssetCreationForm
    template_name = 'assetmasterapp/create.html'

    def get_success_url(self):
        return reverse('assetmasterapp:list')


class AssetDetailView(DetailView, FormMixin):
    model = Asset
    form_class = EquityTransactionCreationForm
    context_object_name = 'target_asset'
    template_name = 'assetmasterapp/detail.html'

    def get_context_data(self, **kwargs):
        context = super(AssetDetailView, self).get_context_data(**kwargs)

        # Getting asset id from my portfolio
        my_portfolio_scalar_query = Portfolio.objects.filter(owner=self.request.user).values()
        if my_portfolio_scalar_query:
            for my_portfolio in my_portfolio_scalar_query:
                my_portfolio_pk = my_portfolio['id']
                target_user_id = my_portfolio['owner_id']
                context.update({'my_portfolio_pk': my_portfolio_pk})
                context.update({'target_user_id': target_user_id})

            my_equity_scalar_query = Equity.objects.filter(portfolio=my_portfolio_pk, asset=self.object.pk).values()
            if my_equity_scalar_query:
                for my_equity in my_equity_scalar_query:
                    my_equity_pk = my_equity['id']
                context.update({'my_equity_asset': my_equity})

                # Equity Transactions
                equity_transaction_query = EquityTransaction.objects.filter(equity=my_equity_pk).order_by('-transaction_date').values()
                if equity_transaction_query:
                    context.update({'equity_transaction': equity_transaction_query})

        return context


class AssetUpdateView(UpdateView):
    model = Asset
    form_class = AssetCreationForm
    context_object_name = 'target_asset'
    template_name = 'assetmasterapp/update.html'

    def get_success_url(self):
        return reverse('assetmasterapp:detail',kwargs={'pk':self.object.pk})


class AssetDeleteView(DeleteView):
    model = Asset
    context_object_name = 'target_asset'
    template_name = 'assetmasterapp/delete.html'

    def get_success_url(self):
        return reverse('assetmasterapp:list')