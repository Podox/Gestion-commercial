# urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),  # Assuming you have an index view
    path('client/', views.client_view, name='client'),  # New URL pattern for client view
    # Add other URL patterns here
]
