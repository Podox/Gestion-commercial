from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone
from django.db import models
class Product(models.Model):
    name = models.CharField(max_length=100)
    brand = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.name

class Service(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.name

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
        ('Materiel et Prestation', 'Materiel et Prestation'),
    ]

    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    date_creation = models.DateTimeField(auto_now_add=True)
    type_commande = models.CharField(max_length=30, choices=CLIENT_TYPE_CHOICES, default='Prestation')
    products = models.ManyToManyField(Product, through='CommandeProduct', related_name='commands')
    services = models.ManyToManyField(Service, through='CommandeService', related_name='commands')

    def __str__(self):
        return f"Commande {self.id} for {self.client}"

class CommandeProduct(models.Model):
    command = models.ForeignKey(Command, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.product.name} (x{self.quantity}) in Commande {self.command.id}"

class CommandeService(models.Model):
    command = models.ForeignKey(Command, on_delete=models.CASCADE)
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.service.name} (x{self.quantity}) in Commande {self.command.id}"
class Offre(models.Model):
    date_creation = models.DateTimeField(default=timezone.now)
    command = models.ForeignKey(Command, on_delete=models.CASCADE)
    profit_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)  # Profit margin as an amount

    def __str__(self):
        return f"Offre {self.id} for {self.command.client.prenom} {self.command.client.nom}"

    def calculate_total(self):
        # Calculate total price for products in the command
        total_products = sum(
            cp.product.price * cp.quantity for cp in self.command.commandeproduct_set.all()
        )
        # Calculate total price for services in the command
        total_services = sum(
            cs.service.price * cs.quantity for cs in self.command.commandeservice_set.all()
        )
        # Calculate total with profit amount
        total = total_products + total_services
        total_with_profit = total + self.profit_amount
        return total_with_profit

class Fournisseur(models.Model):
    nom = models.CharField(max_length=100)
    prenom = models.CharField(max_length=100, null=True, blank=True)
    email = models.EmailField()
    adresse = models.CharField(max_length=200, null=True, blank=True)
    numero_telephone = models.CharField(max_length=15, null=True, blank=True)
    date_ajout = models.DateTimeField(default=timezone.now)
    commande = models.ManyToManyField(Command)  # ManyToManyField for multiple commandes

    def __str__(self):
        return f"{self.nom} {self.prenom}"
#gg