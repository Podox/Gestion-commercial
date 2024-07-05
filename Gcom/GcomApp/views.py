# views.py
from django.shortcuts import render

def index(request):
    return render(request, 'index.html')

def client_view(request):
    return render(request, 'client.html')
