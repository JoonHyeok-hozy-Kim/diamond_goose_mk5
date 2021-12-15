from django.urls import path

from hozylabapp.views import HozyLabHomeView, import_excel

app_name = 'hozylabapp'

urlpatterns = [

    path('lab_home/',HozyLabHomeView.as_view(),name='lab_home'),

    path('import_excel/', import_excel, name='import_excel'),
]