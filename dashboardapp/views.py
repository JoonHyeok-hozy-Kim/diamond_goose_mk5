from django.contrib.auth.decorators import login_required
from django.shortcuts import render

# Create your views here.
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views.generic import CreateView, DetailView
from django.views.generic.edit import FormMixin

from dashboardapp.decorators import dashboard_ownership_required
from dashboardapp.forms import DashboardCreationForm
from dashboardapp.models import Dashboard
from portfolioapp.forms import PortfolioCreationForm

has_ownership = [login_required, dashboard_ownership_required]


class DashboardCreateView(CreateView):
    model = Dashboard
    form_class = DashboardCreationForm
    context_object_name = 'target_dashboard'
    template_name = 'dashboardapp/create.html'

    def form_valid(self, form):
        target_dashboard = form.save(commit=False)
        target_dashboard.owner = self.request.user
        target_dashboard.save()

        return super().form_valid(form)

    def get_success_url(self):
        return reverse('dashboardapp:detail', kwargs={'pk':self.object.pk})


@method_decorator(has_ownership,'get')
class DashboardDetailView(DetailView, FormMixin):
    model = Dashboard
    context_object_name = 'target_dashboard'
    form_class = PortfolioCreationForm
    template_name = 'dashboardapp/detail.html'

    def get_context_data(self, **kwargs):
        context = super(DashboardDetailView, self).get_context_data(**kwargs)

        target_portfolio_query = Dashboard.objects.filter(owner=self.request.user).values()
        if target_portfolio_query:
            target_portfolio_pk = target_portfolio_query[0]['owner_id']
            context.update({'target_portfolio_pk': target_portfolio_pk})

        return context