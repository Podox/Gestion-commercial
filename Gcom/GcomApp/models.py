from django.contrib.auth.models import User
from django.db import models

from django.db import models

class Client(models.Model):
    nom = models.CharField(max_length=100)
    prenom = models.CharField(max_length=100)
    entreprise = models.CharField(max_length=100)
    adresse = models.CharField(max_length=200)
    mail = models.EmailField()
    numero_telephone = models.CharField(max_length=15)

    def __str__(self):
        return f"{self.prenom} {self.nom}"

class Command(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    commande = models.TextField()

    def __str__(self):
        return f"Commande {self.id} for {self.client}"

class Offre(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    Offre = models.TextField()

    def __str__(self):
        return f"Offre {self.id} for {self.client.prenom} {self.client.nom}"
    
