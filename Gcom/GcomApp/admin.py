from django.contrib import admin
from .models import Client, Command, Offre,Status,Fournisseur

admin.site.register(Client)
admin.site.register(Command)
admin.site.register(Offre)
admin.site.register(Status)
admin.site.register(Fournisseur)