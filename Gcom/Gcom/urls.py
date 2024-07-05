# Gcom/urls.py

from django.contrib import admin
from django.urls import path, include
from django.contrib.auth.decorators import login_required
from GcomApp import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.login_view, name='login'),
    path('index/', login_required(views.index), name='index'),  # Protect the index view
    # Include the app's URLs
    path('app/', include('GcomApp.urls')),
]
