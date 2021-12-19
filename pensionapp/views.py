from django.shortcuts import render

# Create your views here.
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, ListView, DetailView
from django.views.generic.edit import FormMixin, DeleteView

from dashboardapp.models import Dashboard
from pensionapp.forms import PensionCreationForm, PensionTransactionCreationForm
from pensionapp.models import Pension, PensionTransaction


class PensionCreateView(CreateView):
    model = Pension
    form_class = PensionCreationForm
    template_name = 'pensionapp/pension_create.html'

    def form_valid(self, form):
        temp_pension = form.save(commit=False)
        temp_pension.owner = self.request.user
        temp_pension.dashboard = Dashboard.objects.get(owner=self.request.user)
        temp_pension.save()

        return super().form_valid(form)

    def get_success_url(self):
        return reverse('pensionapp:pension_list')


class PensionListView(ListView):
    model = Pension
    context_object_name = 'pension_list'
    template_name = 'pensionapp/pension_list.html'


class PensionDetailView(DetailView, FormMixin):
    model = Pension
    form_class = PensionTransactionCreationForm
    context_object_name = 'target_pension'
    template_name = 'pensionapp/pension_detail.html'


class PensionTransactionCreateView(CreateView):
    model = PensionTransaction
    form_class = PensionTransactionCreationForm
    template_name = 'pensionapp/pensiontransaction_create.html'

    def form_valid(self, form):
        temp_pension_transaction = form.save(commit=False)
        temp_pension_transaction.owner = self.request.user
        print('self.request.POST : ',self.request.POST)
        temp_pension_transaction.pension = Pension.objects.get(pk=self.request.POST['pension_pk'])
        temp_pension_transaction.save()

        temp_pension_transaction.pension.calculate_total_paid_amount()

        return super().form_valid(form)

    def get_success_url(self):
        return reverse('pensionapp:pension_detail',kwargs={'pk':self.request.POST['pension_pk']})


class PensionTransactionDetailView(DetailView, FormMixin):
    model = PensionTransaction
    form_class = PensionTransactionCreationForm
    template_name = 'pensionapp/pensiontransaction_detail.html'


class PensionTransactionDeleteView(DeleteView):
    model = PensionTransaction
    context_object_name = 'target_pension_transaction'
    template_name = 'pensionapp/pensiontransaction_delete.html'