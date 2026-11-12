from django.urls import path
from .views import GenerateQuittanceView, ListQuittanceView

urlpatterns = [
    path('ListQuittance', ListQuittanceView.as_view(), name='list_quittances'),
    path('genereQuittance', GenerateQuittanceView.as_view(), name='generer_quittance'),
]