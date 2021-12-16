from django.urls import path

from pensionapp.views import PensionCreateView, PensionListView, PensionDetailView

app_name = 'pensionapp'

urlpatterns = [
    path('pension_create/',PensionCreateView.as_view(),name='pension_create'),
    path('pension_list/',PensionListView.as_view(),name='pension_list'),
    path('pension_detail/<int:pk>',PensionDetailView.as_view(),name='pension_detail'),
    # path('delete/<int:pk>',EquityTransactionDeleteView.as_view(),name='delete'),

    # path('import_csv/', import_csv, name='import_csv'),
    # path('export_csv_template/', export_csv_template, name='export_csv_template'),
]