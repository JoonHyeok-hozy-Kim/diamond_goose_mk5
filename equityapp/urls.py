from django.urls import path

from equityapp.views import EquityCreateView, EquityDetailView

app_name = 'equityapp'

urlpatterns = [

    path('create/',EquityCreateView.as_view(), name='create'),
    path('detail/<int:pk>',EquityDetailView.as_view(), name='detail'),
    # path('list/',EquityListView.as_view(), name='list'),

]