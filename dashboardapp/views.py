from django.shortcuts import render

# Create your views here.
from django.urls import reverse
from django.views.generic import CreateView, DetailView

from dashboardapp.forms import DashboardCreationForm
from dashboardapp.models import Dashboard


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


class DashboardDetailView(DetailView):
    model = Dashboard
    context_object_name = 'target_dashboard'
    template_name = 'dashboardapp/detail.html'