from django.shortcuts import render
from django.contrib.auth import logout
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from .forms import RegistrationForm
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
# Create your views here.

# Main page
def index(request):
    return render(request, "auctions/index.html")

def register(request):
    if request.method == "POST":
        user_form = RegistrationForm(request.POST)
        if user_form.is_valid():
            # if valid -> create user, but not saving it!
            new_user = user_form.save(commit=False)
            # Set password
            new_user.set_password(
                user_form.cleaned_data["password"]
            )
            # Save user
            new_user.save()
            return render(request, "auctions/register_done.html", {
                "new_user": new_user
            })
    else:
        user_form = RegistrationForm()
    return render(request, "auctions/register.html", {
        "user_form": user_form
    })