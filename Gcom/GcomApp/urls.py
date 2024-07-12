# urls.py

from django.urls import path
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView, LogoutView
from . import views
urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('', views.index, name='index'),
    # Client
    path('clients/', views.client_list, name='client_list'),
    path('clients/add/', views.client_add, name='client_add'),
    path('clients/<int:client_id>/edit/', views.client_edit, name='client_edit'),
    path('clients/<int:client_id>/delete/', views.client_delete, name='client_delete'),
    path('Gclient/', views.Gclient_view, name='Gclient'), 
    path('client/timeline/', views.client_timeline, name='client_timeline'),
    path('Gclient/', views.Gclient_view, name='Gclient'),  
    #Commande
    path('commande/', views.commandes_view, name='commande_list'),
    #offre
    path('offre/', views.offre_list, name='offre_list'),
    #fornisseur
    path('fournisseur/', views.fournisseur_list, name='fournisseur_list'),
    path('fournisseur/timeline/', views.fournisseur_timeline, name='fournisseur_timeline'),
]
