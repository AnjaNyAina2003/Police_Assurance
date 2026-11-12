from django.urls import path
from .views import AddClientView, ClientListView, ClientView, SearchClientView

urlpatterns = [
    path('Listclients', ClientListView.as_view(), name='liste_clients'),
    path('searchclients', SearchClientView.as_view(), name='recherche client'),
    path('clients', AddClientView.as_view(), name='creer et recupere client'),
    path('clients/<int:pk>', ClientView.as_view(), name='detail_client'),
]