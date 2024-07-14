from django.contrib import admin
from .models import Status, Client, Command, Offre, Fournisseur, Product, Service, CommandeProduct, CommandeService

class ClientAdmin(admin.ModelAdmin):
    list_display = ('nom', 'prenom', 'entreprise', 'mail', 'date_creation')
    search_fields = ('nom', 'prenom', 'entreprise', 'mail')

class CommandeProductInline(admin.TabularInline):
    model = CommandeProduct
    extra = 1

class CommandeServiceInline(admin.TabularInline):
    model = CommandeService
    extra = 1

class CommandAdmin(admin.ModelAdmin):
    list_display = ('id', 'client', 'type_commande', 'date_creation')
    search_fields = ('client__nom', 'client__prenom', 'type_commande')
    inlines = [CommandeProductInline, CommandeServiceInline]

class OffreAdmin(admin.ModelAdmin):
    list_display = ('id', 'client', 'date_creation')
    search_fields = ('client__nom', 'client__prenom', 'description')

class FournisseurAdmin(admin.ModelAdmin):
    list_display = ('nom', 'prenom', 'email', 'date_ajout')
    search_fields = ('nom', 'prenom', 'email')

class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'brand', 'price')
    search_fields = ('name', 'brand')

class ServiceAdmin(admin.ModelAdmin):
    list_display = ('name', 'price')
    search_fields = ('name',)

admin.site.register(Status)
admin.site.register(Client, ClientAdmin)
admin.site.register(Command, CommandAdmin)
admin.site.register(Offre, OffreAdmin)
admin.site.register(Fournisseur, FournisseurAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Service, ServiceAdmin)
