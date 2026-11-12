from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from . import views

urlpatterns = [
    path('auth/', views.authentification, name="login et sign-in"),
    path('login/', views.login, name='login'),
    path('home/', views.home, name='home'),
    path('logout/', views.logout, name='logout'),
    path('register/', views.register, name='register'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('branche/', views.branche, name='branche'),
    path('user/', views.user, name='user'),
    path('agence/', views.agence, name='agence'),
    path('client/', views.client, name='client'),
    path('searchClient/', views.searchClient, name='searchClient'),
    path('police/', views.police_assurance, name='police'),
    path('historique/', views.historique, name='historique'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)