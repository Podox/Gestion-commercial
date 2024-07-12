# GcomApp/views.py

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.contrib import messages 
from GcomApp.models import Client, Command, Offre, Fournisseur,Status
from django.db.models import Count
from django.utils import timezone
from django.db.models.functions import TruncMonth

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        if username == 'agora' and password == 'agora123':
            user = authenticate(request, username=username, password=password)
            if user is None:
                # Create the user if it doesn't exist
                from django.contrib.auth.models import User
                user = User.objects.create_user(username='agora', password='agora123')
            login(request, user)
            return redirect('index')  # Redirect to index after login
        else:
            messages.error(request, "Invalid login details. Please try again.")  # Add error message
    return render(request, 'login.html')

@login_required
def logout_view(request):
    # Clear the session data
    request.session.flush()
    return render(request, 'login.html')

@login_required
def index(request):
    # Get the count of clients
    client_count = Client.objects.count()

    # Get the count of commands
    command_count = Command.objects.count()

    # Get the count of fournisseurs
    fournisseur_count = Fournisseur.objects.count()

    # Get the count of offers
    offre_count = Offre.objects.count()

    # Get the count of clients with a status "Commande confirmer"
    confirmed_status = Status.objects.filter(name="Commande confirmer").first()
    if confirmed_status:
        confirmed_clients_count = Client.objects.filter(status=confirmed_status).distinct().count()
    else:
        confirmed_clients_count = 0

    # Get the count of clients created per month for the current year
    current_year = timezone.now().year
    clients_by_month = (
        Client.objects.filter(date_creation__year=current_year)
        .annotate(month=TruncMonth('date_creation'))
        .values('month')
        .annotate(count=Count('id'))
        .order_by('month')
    )

    # Get the count of commands created per month for the current year
    commands_by_month = (
        Command.objects.filter(date_creation__year=current_year)
        .annotate(month=TruncMonth('date_creation'))
        .values('month')
        .annotate(count=Count('id'))
        .order_by('month')
    )

    # Format the data for the client creation chart
    monthly_client_data = {month: 0 for month in range(1, 13)}
    for entry in clients_by_month:
        monthly_client_data[entry['month'].month] = entry['count']

    # Format the data for the command creation chart
    monthly_command_data = {month: 0 for month in range(1, 13)}
    for entry in commands_by_month:
        monthly_command_data[entry['month'].month] = entry['count']

    # Context dictionary to pass data to the template
    context = {
        'client_count': client_count,
        'command_count': command_count,
        'fournisseur_count': fournisseur_count,
        'offre_count': offre_count,
        'confirmed_clients_count': confirmed_clients_count,
        'monthly_client_data': monthly_client_data,
        'monthly_command_data': monthly_command_data,
    }

    return render(request, 'index.html', context)

@login_required
def client_view(request):
    return render(request, 'client.html')

@login_required
def client_list(request):
    clients = Client.objects.all()
    return render(request, 'clients.html', {'clients': clients})

@login_required
def client_timeline(request):
    # Get the selected client ID from the query parameters
    selected_client_id = request.GET.get('client_id')

    # Fetch all clients to populate the dropdown
    clients = Client.objects.all()

    # Initialize variables for the selected client and their events
    selected_client = None
    client_events = []

    if selected_client_id:
        # Fetch the selected client based on the ID
        selected_client = get_object_or_404(Client, id=selected_client_id)

        # Fetch commands and offers for the selected client, ordered by creation date
        commands = Command.objects.filter(client=selected_client).order_by('date_creation')
        offres = Offre.objects.filter(client=selected_client).order_by('date_creation')

        # Collect command events
        for command in commands:
            client_events.append({
                'date': command.date_creation,
                'title': f"Commande de type: {command.type_commande}",
                'description': command.commande
            })

        # Collect offer events
        for offre in offres:
            client_events.append({
                'date': offre.date_creation,
                'title': f'Offre {offre.id}',
                'description': offre.description
            })

        # Sort events by date
        client_events.sort(key=lambda x: x['date'], reverse=True)

    # Prepare the context for the template
    context = {
        'clients': clients,
        'selected_client': selected_client,
        'client_events': client_events
    }

    # Render the template with the context
    return render(request, 'client_timeline.html', context)

@login_required
def fournisseur_list(request):
    fournisseurs = Fournisseur.objects.all()
    return render(request, 'fournisseur.html', {'fournisseurs': fournisseurs})

@login_required
def fournisseur_timeline(request):
    selected_fournisseur_id = request.GET.get('fournisseur_id')
    fournisseurs = Fournisseur.objects.all()
    selected_fournisseur = None
    fournisseur_events = []

    if selected_fournisseur_id:
        selected_fournisseur = get_object_or_404(Fournisseur, id=selected_fournisseur_id)
        commands = Command.objects.filter(fournisseur=selected_fournisseur).order_by('date_creation')

        for command in commands:
            fournisseur_events.append({
                'date': command.date_creation,
                'title': f'Commande {command.id}',
                'description': command.commande
            })

        fournisseur_events.sort(key=lambda x: x['date'], reverse=True)

    context = {
        'fournisseurs': fournisseurs,
        'selected_fournisseur': selected_fournisseur,
        'fournisseur_events': fournisseur_events
    }

    return render(request, 'fournisseur_timeline.html', context)

@login_required
def commandes_view(request):
    commandes = Command.objects.all()
    return render(request, 'commande.html', {'commandes': commandes})

@login_required
def offre_list(request):
    offres = Offre.objects.all()
    return render(request, 'offre.html', {'offres': offres})