# urls.py

from django.urls import path
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView, LogoutView
from . import views

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('', login_required(views.index), name='index'),  # Protect the index view
    path('client/', login_required(views.client_view), name='client'),
    # Add other URL patterns here
]
