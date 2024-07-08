# GcomApp/views.py

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.contrib import messages  # Import messages
from GcomApp.models import Client

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
    return render(request, 'index.html')

@login_required
def client_view(request):
    return render(request, 'client.html')

@login_required
def client_list(request):
    clients = Client.objects.all()
    return render(request, 'clients.html', {'clients': clients})

# Add other views as needed
