#views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse
from django.contrib import messages 
from GcomApp.models import Client, Command, Offre, Fournisseur, Status, Product, Service, CommandeProduct, CommandeService
from django.db.models import Count
from django.utils import timezone
from django.db.models.functions import TruncMonth
from .forms import ProductForm, ServiceForm, CommandForm,SelectFournisseurForm, AssignCommandsForm,OffreForm
from django.views.decorators.csrf import csrf_exempt
from django.urls import reverse


######################################         LOGIN PAGE                #####################################################
def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        if username == 'agora' and password == 'agora123':
            user = authenticate(request, username=username, password=password)
            if user is None:
                from django.contrib.auth.models import User
                user = User.objects.create_user(username='agora', password='agora123')
            login(request, user)
            return redirect('index')
        else:
            messages.error(request, "Invalid login details. Please try again.")
    return render(request, 'login.html')

@login_required
def logout_view(request):
    request.session.flush()
    return render(request, 'login.html')

@login_required
def index(request):
    client_count = Client.objects.count()
    command_count = Command.objects.count()
    fournisseur_count = Fournisseur.objects.count()
    offre_count = Offre.objects.count()
    confirmed_status = Status.objects.filter(name="Commande confirmer").first()
    confirmed_clients_count = Client.objects.filter(status=confirmed_status).distinct().count() if confirmed_status else 0
    current_year = timezone.now().year
    clients_by_month = (
        Client.objects.filter(date_creation__year=current_year)
        .annotate(month=TruncMonth('date_creation'))
        .values('month')
        .annotate(count=Count('id'))
        .order_by('month')
    )
    commands_by_month = (
        Command.objects.filter(date_creation__year=current_year)
        .annotate(month=TruncMonth('date_creation'))
        .values('month')
        .annotate(count=Count('id'))
        .order_by('month')
    )
    monthly_client_data = {month: 0 for month in range(1, 13)}
    for entry in clients_by_month:
        monthly_client_data[entry['month'].month] = entry['count']
    monthly_command_data = {month: 0 for month in range(1, 13)}
    for entry in commands_by_month:
        monthly_command_data[entry['month'].month] = entry['count']
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
###############################################         CLIENT                #####################################################
@login_required
def client_list(request):
    clients = Client.objects.all()
    return render(request, 'clients.html', {'clients': clients})

@login_required
def client_timeline(request):
    selected_client_id = request.GET.get('client_id')
    clients = Client.objects.all()
    selected_client = None
    client_events = []

    if selected_client_id:
        selected_client = get_object_or_404(Client, id=selected_client_id)
        commands = Command.objects.filter(client=selected_client).order_by('date_creation')
        for command in commands:
            client_events.append({
                'date': command.date_creation,
                'title': f"Commande de type: {command.type_commande}",
                'description': command.id
            })
        
        offres = Offre.objects.filter(command__client=selected_client).order_by('date_creation')
        for offre in offres:
            client_events.append({
                'date': offre.date_creation,
                'title': f'Offre {offre.id}',
                'description': offre.description
            })

        client_events.sort(key=lambda x: x['date'], reverse=True)

    context = {
        'clients': clients,
        'selected_client': selected_client,
        'client_events': client_events
    }
    return render(request, 'client_timeline.html', context)

@login_required
def Gclient_view(request):
    clients = Client.objects.all()
    statuses = Status.objects.all()
    return render(request, 'Gclient.html', {'clients': clients, 'statuses': statuses})

@login_required
def client_add(request):
    if request.method == 'POST':
        prenom = request.POST.get('prenom')
        nom = request.POST.get('nom')
        entreprise = request.POST.get('entreprise')
        mail = request.POST.get('mail')
        numero_telephone = request.POST.get('numero_telephone')
        status_ids = request.POST.getlist('status')
        client = Client.objects.create(
            prenom=prenom,
            nom=nom,
            entreprise=entreprise,
            mail=mail,
            numero_telephone=numero_telephone
        )
        client.status.set(status_ids)
        client.save()
        response_data = {
            'id': client.id,
            'prenom': client.prenom,
            'nom': client.nom,
            'entreprise': client.entreprise,
            'mail': client.mail,
            'numero_telephone': client.numero_telephone,
            'date_creation': client.date_creation,
            'status': [status.name for status in client.status.all()]
        }
        return JsonResponse(response_data)
    return JsonResponse({'error': 'Invalid request'}, status=400)

@login_required
def client_edit(request, client_id):
    client = get_object_or_404(Client, id=client_id)
    if request.method == 'POST':
        client.prenom = request.POST.get('prenom')
        client.nom = request.POST.get('nom')
        client.entreprise = request.POST.get('entreprise')
        client.mail = request.POST.get('mail')
        client.numero_telephone = request.POST.get('numero_telephone')
        status_ids = request.POST.getlist('status')
        client.status.set(status_ids)
        client.save()
        response_data = {
            'id': client.id,
            'prenom': client.prenom,
            'nom': client.nom,
            'entreprise': client.entreprise,
            'mail': client.mail,
            'numero_telephone': client.numero_telephone,
            'date_creation': client.date_creation,
            'status': [status.name for status in client.status.all()]
        }
        return JsonResponse(response_data)
    response_data = {
        'id': client.id,
        'prenom': client.prenom,
        'nom': client.nom,
        'entreprise': client.entreprise,
        'mail': client.mail,
        'numero_telephone': client.numero_telephone,
        'status': [status.id for status in client.status.all()]
    }
    return JsonResponse(response_data)

@login_required
def client_delete(request, client_id):
    client = get_object_or_404(Client, id=client_id)
    client.delete()
    return JsonResponse({'result': 'ok'})

###############################################         FOURNISSEUR               #####################################################
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
                'description': f'{command.client.prenom} {command.client.nom}'
            })
        
        fournisseur_events.sort(key=lambda x: x['date'], reverse=True)
    context = {
        'fournisseurs': fournisseurs,
        'selected_fournisseur': selected_fournisseur,
        'fournisseur_events': fournisseur_events
    }
    return render(request, 'fournisseur_timeline.html', context)
@login_required
def Gfournisseur_view(request):
    fournisseurs = Fournisseur.objects.all()
    return render(request, 'Gfournisseur.html', {'fournisseurs': fournisseurs})

@login_required
def fournisseur_add(request):
    if request.method == 'POST':
        prenom = request.POST.get('prenom')
        nom = request.POST.get('nom')
        email = request.POST.get('email')
        adresse = request.POST.get('adresse')
        numero_telephone = request.POST.get('numero_telephone')
        fournisseur = Fournisseur.objects.create(
            prenom=prenom,
            nom=nom,
            email=email,
            adresse=adresse,
            numero_telephone=numero_telephone
        )
        response_data = {
            'id': fournisseur.id,
            'prenom': fournisseur.prenom,
            'nom': fournisseur.nom,
            'email': fournisseur.email,
            'adresse': fournisseur.adresse,
            'numero_telephone': fournisseur.numero_telephone,
            'date_ajout': fournisseur.date_ajout
        }
        return JsonResponse(response_data)
    return JsonResponse({'error': 'Invalid request'}, status=400)

@login_required
def fournisseur_edit(request, fournisseur_id):
    fournisseur = get_object_or_404(Fournisseur, id=fournisseur_id)
    if request.method == 'POST':
        fournisseur.prenom = request.POST.get('prenom')
        fournisseur.nom = request.POST.get('nom')
        fournisseur.email = request.POST.get('email')
        fournisseur.adresse = request.POST.get('adresse')
        fournisseur.numero_telephone = request.POST.get('numero_telephone')
        fournisseur.save()
        response_data = {
            'id': fournisseur.id,
            'prenom': fournisseur.prenom,
            'nom': fournisseur.nom,
            'email': fournisseur.email,
            'adresse': fournisseur.adresse,
            'numero_telephone': fournisseur.numero_telephone,
            'date_ajout': fournisseur.date_ajout
        }
        return JsonResponse(response_data)
    response_data = {
        'id': fournisseur.id,
        'prenom': fournisseur.prenom,
        'nom': fournisseur.nom,
        'email': fournisseur.email,
        'adresse': fournisseur.adresse,
        'numero_telephone': fournisseur.numero_telephone
    }
    return JsonResponse(response_data)

@login_required
def fournisseur_delete(request, fournisseur_id):
    fournisseur = get_object_or_404(Fournisseur, id=fournisseur_id)
    fournisseur.delete()
    return JsonResponse({'result': 'ok'})
@login_required
def select_fournisseur(request):
    if request.method == 'POST':
        form = SelectFournisseurForm(request.POST)
        if form.is_valid():
            fournisseur = form.cleaned_data['fournisseur']
            return redirect('assign_commands', fournisseur_id=fournisseur.id)
    else:
        form = SelectFournisseurForm()
    return render(request, 'select_fournisseur.html', {'form': form})
###############################################         COMMANDES                #####################################################
@login_required
def commandes_view(request):
    commandes = Command.objects.all()
    return render(request, 'commande.html', {'commandes': commandes})

@login_required
def assign_commands(request, fournisseur_id):
    fournisseur = get_object_or_404(Fournisseur, id=fournisseur_id)
    if request.method == 'POST':
        form = AssignCommandsForm(request.POST, instance=fournisseur)
        if form.is_valid():
            form.save()
            return redirect('select_fournisseur')
    else:
        form = AssignCommandsForm(instance=fournisseur)
    return render(request, 'assign_commands.html', {'form': form, 'fournisseur': fournisseur})

@login_required
def manage_commands(request):
    commandes = Command.objects.all()
    clients = Client.objects.all()
    products = Product.objects.all()
    services = Service.objects.all()
    command_form = CommandForm()
    product_form = ProductForm()
    service_form = ServiceForm()
    return render(request, 'Gcommande.html', {
        'commandes': commandes,
        'clients': clients,
        'products': products,
        'services': services,
        'command_form': command_form,
        'product_form': product_form,
        'service_form': service_form,
    })

@login_required
@csrf_exempt
def commande_edit(request, commande_id):
    commande = get_object_or_404(Command, id=commande_id)
    if request.method == 'POST':
        form = CommandForm(request.POST, instance=commande)
        if form.is_valid():
            commande = form.save()
            CommandeProduct.objects.filter(command=commande).delete()
            for product_id in request.POST.getlist('products'):
                quantity = request.POST.get(f'product_quantity_{product_id}', 1)
                CommandeProduct.objects.create(command=commande, product_id=product_id, quantity=quantity)
            CommandeService.objects.filter(command=commande).delete()
            for service_id in request.POST.getlist('services'):
                quantity = request.POST.get(f'service_quantity_{service_id}', 1)
                CommandeService.objects.create(command=commande, service_id=service_id, quantity=quantity)
            return JsonResponse({'status': 'success'})
    else:
        response_data = {
            'id': commande.id,
            'client_id': commande.client.id,
            'type_commande': commande.type_commande,
            'products': [{'id': cp.product.id, 'name': cp.product.name, 'quantity': cp.quantity} for cp in commande.commandeproduct_set.all()],
            'services': [{'id': cs.service.id, 'name': cs.service.name, 'quantity': cs.quantity} for cs in commande.commandeservice_set.all()]
        }
        return JsonResponse(response_data)

@login_required
@csrf_exempt
def commande_delete(request, commande_id):
    commande = get_object_or_404(Command, id=commande_id)
    if request.method == 'POST':
        commande.delete()
        return JsonResponse({'result': 'ok'})
    return JsonResponse({'error': 'Invalid request'}, status=400)


@login_required
def manage_commands(request):
    commandes = Command.objects.all()
    clients = Client.objects.all()
    products = Product.objects.all()
    services = Service.objects.all()
    command_form = CommandForm()
    product_form = ProductForm()
    service_form = ServiceForm()
    return render(request, 'Gcommande.html', {
        'commandes': commandes,
        'clients': clients,
        'products': products,
        'services': services,
        'command_form': command_form,
        'product_form': product_form,
        'service_form': service_form,
    })

@csrf_exempt
def add_commande(request):
    if request.method == 'POST':
        form = CommandForm(request.POST)
        if form.is_valid():
            commande = form.save()
            for product_id in request.POST.getlist('products'):
                quantity = request.POST.get(f'product_quantity_{product_id}', 1)
                CommandeProduct.objects.create(command=commande, product_id=product_id, quantity=quantity)
            for service_id in request.POST.getlist('services'):
                quantity = request.POST.get(f'service_quantity_{service_id}', 1)
                CommandeService.objects.create(command=commande, service_id=service_id, quantity=quantity)
            return JsonResponse({'status': 'success'})
        else:
            return JsonResponse({'errors': form.errors}, status=400)
    return JsonResponse({'error': 'Invalid request'}, status=400)

###############################################         OFFRE                #####################################################
@login_required
def offre_list(request):
    offres = Offre.objects.all()
    # Calculate the total profit and the total amount for products and services
    total_profit = sum(offre.profit_amount for offre in offres)
    total_products_services = sum(offre.calculate_total() for offre in offres)

    return render(request, 'offre.html', {
        'offres': offres,
        'total_profit': total_profit,
        'total_products_services': total_products_services
    })

def create_offre(request):
    if request.method == 'POST':
        form = OffreForm(request.POST)
        if form.is_valid():
            offre = form.save()
            # Redirect to the receipt view after successful offer creation
            return redirect('receipt_view', offre_id=offre.id)
    else:
        form = OffreForm()
    
    return render(request, 'create_offre.html', {'form': form})

def receipt_view(request, offre_id):
    offre = get_object_or_404(Offre, id=offre_id)
    products = CommandeProduct.objects.filter(command=offre.command)
    services = CommandeService.objects.filter(command=offre.command)
    total_with_profit = offre.calculate_total()

    context = {
        'offre': offre,
        'products': products,
        'services': services,
        'total_with_profit': total_with_profit,
    }

    return render(request, 'receipt.html', context)

def get_commands(request):
    client_id = request.GET.get('client_id')
    commands = Command.objects.filter(client_id=client_id).values('id')
    return JsonResponse({'commands': list(commands)})




###############################################         PRODUIT                #####################################################

@login_required
def Gproduct_view(request):
    products = Product.objects.all()
    return render(request, 'Gproduct.html', {'products': products})


@csrf_exempt
def product_add(request):
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            product = form.save()
            return JsonResponse({'id': product.id, 'name': product.name, 'brand': product.brand, 'price': product.price})
        else:
            return JsonResponse({'errors': form.errors}, status=400)
    return JsonResponse({'error': 'Invalid request'}, status=400)

@csrf_exempt
def product_edit(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    if request.method == 'POST':
        form = ProductForm(request.POST, instance=product)
        if form.is_valid():
            product = form.save()
            return JsonResponse({'id': product.id, 'name': product.name, 'brand': product.brand, 'price': product.price})
        else:
            return JsonResponse({'errors': form.errors}, status=400)
    elif request.method == 'GET':
        return JsonResponse({'id': product.id, 'name': product.name, 'brand': product.brand, 'price': product.price})
    return JsonResponse({'error': 'Invalid request'}, status=400)

@csrf_exempt
def product_delete(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    if request.method == 'POST':
        product.delete()
        return JsonResponse({'result': 'ok'})
    return JsonResponse({'error': 'Invalid request'}, status=400)

@login_required
def product_list(request):
    products = Product.objects.all()
    return render(request, 'product_list.html', {'products': products})

@csrf_exempt
def add_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            product = form.save()
            return JsonResponse({'id': product.id, 'name': product.name})
        else:
            return JsonResponse({'errors': form.errors}, status=400)
    return JsonResponse({'error': 'Invalid request'}, status=400)

###############################################         SERVICE                #####################################################
@login_required
def Gservice_view(request):
    services = Service.objects.all()
    return render(request, 'Gservice.html', {'services': services})


@csrf_exempt
def service_add(request):
    if request.method == 'POST':
        form = ServiceForm(request.POST)
        if form.is_valid():
            service = form.save()
            return JsonResponse({'id': service.id, 'name': service.name, 'price': service.price})
        else:
            return JsonResponse({'errors': form.errors}, status=400)
    return JsonResponse({'error': 'Invalid request'}, status=400)

@csrf_exempt
def service_edit(request, service_id):
    service = get_object_or_404(Service, id=service_id)
    if request.method == 'POST':
        form = ServiceForm(request.POST, instance=service)
        if form.is_valid():
            service = form.save()
            return JsonResponse({'id': service.id, 'name': service.name, 'price': service.price})
        else:
            return JsonResponse({'errors': form.errors}, status=400)
    elif request.method == 'GET':
        return JsonResponse({'id': service.id, 'name': service.name, 'price': service.price})
    return JsonResponse({'error': 'Invalid request'}, status=400)

@csrf_exempt
def service_delete(request, service_id):
    service = get_object_or_404(Service, id=service_id)
    if request.method == 'POST':
        service.delete()
        return JsonResponse({'result': 'ok'})
    return JsonResponse({'error': 'Invalid request'}, status=400)

@login_required
def service_list(request):
    services = Service.objects.all()
    return render(request, 'service_list.html', {'services': services})

@csrf_exempt
def add_service(request):
    if request.method == 'POST':
        form = ServiceForm(request.POST)
        if form.is_valid():
            service = form.save()
            return JsonResponse({'id': service.id, 'name': service.name})
        else:
            return JsonResponse({'errors': form.errors}, status=400)
    return JsonResponse({'error': 'Invalid request'}, status=400)

