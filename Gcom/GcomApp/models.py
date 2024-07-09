from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone
from django.db import models

class Status(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Client(models.Model):
    nom = models.CharField(max_length=100)
    prenom = models.CharField(max_length=100)
    entreprise = models.CharField(max_length=100)
    adresse = models.CharField(max_length=200)
    mail = models.EmailField()
    numero_telephone = models.CharField(max_length=15)
    date_creation = models.DateTimeField(default=timezone.now)
    status = models.ManyToManyField(Status, related_name='clients')

    def __str__(self):
        return f"{self.prenom} {self.nom}"

class Command(models.Model):
    CLIENT_TYPE_CHOICES = [
        ('Prestation', 'Prestation'),
        ('Materiel', 'Materiel'),
        ('Les-deux', 'Les-deux'),
    ]

    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    commande = models.TextField()
    date_creation = models.DateTimeField(auto_now_add=True)
    type_commande = models.CharField(max_length=20, choices=CLIENT_TYPE_CHOICES, default='Prestation')
    date_creation = models.DateTimeField(default=timezone.now)
    
    def __str__(self):
        return f"Commande {self.id} for {self.client}"

class Offre(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    description = models.TextField()
    date_creation = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Offre {self.id} for {self.client.prenom} {self.client.nom}"

class Fournisseur(models.Model):
    nom = models.CharField(max_length=100)
    prenom = models.CharField(max_length=100, null=True, blank=True)  # Add first name
    email = models.EmailField()
    adresse = models.CharField(max_length=200, null=True, blank=True)  # Add address
    numero_telephone = models.CharField(max_length=15, null=True, blank=True)  # Add phone number
    date_ajout = models.DateTimeField(default=timezone.now)
    commande = models.ForeignKey('Command', on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.nom} {self.prenom}"
#gg