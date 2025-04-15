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
    path("edit/", views.edit, name="edit"),
    # change password urls
    path(
        'password-change/',
        auth_views.PasswordChangeView.as_view(),
        name='password_change'
        ),
    path(
        'password-change/done/',
        auth_views.PasswordChangeDoneView.as_view(),
        name='password_change_done'
        ),
]