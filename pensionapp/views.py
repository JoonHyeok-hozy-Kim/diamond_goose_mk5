from django.shortcuts import render

# Create your views here.
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, ListView, DetailView

from dashboardapp.models import Dashboard
from pensionapp.forms import PensionCreationForm
from pensionapp.models import Pension


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


class PensionDetailView(DetailView):
    model = Pension
    context_object_name = 'target_pension'
    template_name = 'pensionapp/pension_detail.html'