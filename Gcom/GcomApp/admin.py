from django.contrib import admin
from .models import Client, Command, Offre

admin.site.register(Client)
admin.site.register(Command)
admin.site.register(Offre)