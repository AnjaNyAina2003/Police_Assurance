from django.urls import path

from .views import BranchListCreateView, BranchDetailView

urlpatterns = [
    path('branch', BranchListCreateView.as_view(), name='creation et liste branche'),
    path('branch/<int:pk>', BranchDetailView.as_view(), name='modification et suppression branche'),
]