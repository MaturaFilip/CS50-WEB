from django.urls import path, include
from . import views
from django.contrib.auth import views as auth_views

app_name = "auctions"
urlpatterns = [
    path("", views.index, name="index"),
    
    # AUTHENTICATION (build-in)
    # AKA: https://github.com/django/django/blob/stable/5.0.x/django/contrib/auth/urls.py
    path("", include("django.contrib.auth.urls")),
    path("register/", views.register, name="register"),
]