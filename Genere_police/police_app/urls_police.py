from django.urls import path

from .views import  Genere_policeView, List_policeView

urlpatterns = [
    path('ListPolice', List_policeView.as_view(), name='liste_police'),
    path('generePolice', Genere_policeView.as_view(), name='Generer une police assurance')
]