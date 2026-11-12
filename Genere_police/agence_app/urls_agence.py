from django.urls import path
from .views import AgenceListCreateView, AgenceDetailView

urlpatterns = [
    path('agenceLieu', AgenceListCreateView.as_view(), name='creation-et-liste-agence'),
    path('agenceLieu/<int:pk>', AgenceDetailView.as_view(), name='modification-et-suppression-agence'),
]
