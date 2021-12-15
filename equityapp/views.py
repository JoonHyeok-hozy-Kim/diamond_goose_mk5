from django.contrib.auth.decorators import login_required
from django.shortcuts import render

# Create your views here.
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views.generic import CreateView, ListView, DetailView

from assetmasterapp.models import Asset
from equityapp.decorators import equity_ownership_required
from equityapp.forms import EquityCreationForm
from equityapp.models import Equity
from portfolioapp.models import Portfolio

has_ownership = [login_required, equity_ownership_required]


class EquityCreateView(CreateView):
    model = Equity
    form_class = EquityCreationForm
    context_object_name = 'target_equity'
    template_name = 'equityapp/create.html'

    def form_valid(self, form):
        temp_equity = form.save(commit=False)
        temp_equity.owner = self.request.user
        temp_equity.asset = Asset.objects.get(pk=self.request.POST['asset_pk'])
        temp_equity.portfolio = Portfolio.objects.get(owner=self.request.user)
        temp_equity.save()

        return super().form_valid(form)

    def get_success_url(self):
        return reverse('assetmasterapp:detail',kwargs={'pk':self.object.asset.pk})


@method_decorator(has_ownership,'get')
class EquityDetailView(DetailView):
    model = Equity
    template_name = 'equityapp/detail.html'

