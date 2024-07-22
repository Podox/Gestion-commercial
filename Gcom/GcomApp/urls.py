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
    path('manage_commands/', views.manage_commands, name='manage_commands'),
    path('add_product/', views.add_product, name='add_product'),
    path('add_service/', views.add_service, name='add_service'),
    path('add_commande/', views.add_commande, name='add_commande'),
    #offre
    path('offre/', views.offre_list, name='offre_list'),
    path('offre/create/', views.create_offre, name='create_offre'),
    path('offre/<int:offre_id>/receipt/', views.receipt_view, name='receipt_view'),
    path('get_commands/', views.get_commands, name='get_commands'),
    #fornisseur
    path('fournisseurs/', views.fournisseur_list, name='fournisseur_list'),
    path('fournisseurs/add/', views.fournisseur_add, name='fournisseur_add'),
    path('fournisseurs/<int:fournisseur_id>/edit/', views.fournisseur_edit, name='fournisseur_edit'),
    path('fournisseurs/<int:fournisseur_id>/delete/', views.fournisseur_delete, name='fournisseur_delete'),
    path('Gfournisseur/', views.Gfournisseur_view, name='Gfournisseur'),
    path('fournisseur/timeline/', views.fournisseur_timeline, name='fournisseur_timeline'),
     path('select-fournisseur/', views.select_fournisseur, name='select_fournisseur'),
    path('fournisseur/<int:fournisseur_id>/assign-commands/', views.assign_commands, name='assign_commands'),
    # Product
    path('products/', views.product_list, name='product_list'),
    path('products/add/', views.product_add, name='product_add'),
    path('products/<int:product_id>/edit/', views.product_edit, name='product_edit'),
    path('products/<int:product_id>/delete/', views.product_delete, name='product_delete'),
    path('Gproduct/', views.Gproduct_view, name='Gproduct'),
    # Service
    path('services/', views.service_list, name='service_list'),
    path('services/add/', views.service_add, name='service_add'),
    path('services/<int:service_id>/edit/', views.service_edit, name='service_edit'),
    path('services/<int:service_id>/delete/', views.service_delete, name='service_delete'),
    path('Gservice/', views.Gservice_view, name='Gservice'), 
    path('add_product/', views.add_product, name='add_product'),
    path('add_service/', views.add_service, name='add_service'),
    
]
