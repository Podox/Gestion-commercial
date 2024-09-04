#forms.py
from django import forms
from .models import Command, Product, Service,Fournisseur,Offre,Client
class CommandForm(forms.ModelForm):
    class Meta:
        model = Command
        fields = ['client', 'type_commande']

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'brand', 'price']

class ServiceForm(forms.ModelForm):
    class Meta:
        model = Service
        fields = ['name', 'price']

class SelectFournisseurForm(forms.Form):
    fournisseur = forms.ModelChoiceField(queryset=Fournisseur.objects.all(), widget=forms.Select(attrs={'class': 'form-control'}))

class AssignCommandsForm(forms.ModelForm):
    commande = forms.ModelMultipleChoiceField(
        queryset=Command.objects.all(),
        widget=forms.CheckboxSelectMultiple(attrs={'class': 'form-check-input'}),
        required=False
    )

    class Meta:
        model = Fournisseur
        fields = ['commande']

class OffreForm(forms.ModelForm):
    class Meta:
        model = Offre
        fields = ['command', 'profit_amount']
        widgets = {
            'command': forms.Select(attrs={'class': 'form-control'}),
            'profit_amount': forms.NumberInput(attrs={'class': 'form-control'}),
        }