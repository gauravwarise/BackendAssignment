"""
URL configuration for Backend_Assignment_Onfin project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.urls.conf import include
from apps.accounts.views import *
from apps.movies.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('register', UserRegistrationView.as_view(), name='register'),
    path("login", LoginUser.as_view(), name="login"),
    path('movies', MovieView.as_view(), name='movies'),
    path("collection", CollectionView.as_view(), name="collection"),    
    path("collection/<str:uuid>/",CollectionView.as_view(),name="collection-details"),
    path("request-count", RequestCount.as_view(), name="request-count"),
    path("request-count/reset/", RequestCountRest.as_view(), name="request-count-reset"),


]
