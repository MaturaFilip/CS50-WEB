from django.shortcuts import render
from django.contrib.auth import logout
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from .forms import RegistrationForm, UserEditForm, ProfileEditForm
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from .models import Profile, Comment, Bid, Auction
# Create your views here.

# Main page
def index(request):
    auctions = Auction.objects.all()[:5]
    return render(request, "auctions/index.html", {
        "auctions": auctions
    })

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
            # Create the user profile
            Profile.objects.create(user=new_user)

            return render(request, "auctions/register_done.html", {
                "new_user": new_user
            })
    else:
        user_form = RegistrationForm()
    return render(request, "auctions/register.html", {
        "user_form": user_form
    })

@login_required
def edit(request):
    if request.method == "POST":
        user_form = UserEditForm(
            # work with user data
            instance = request.user,
            data = request.POST
        )
        profile_form = ProfileEditForm(
            # work with profile data
            instance = request.user.profile,
            data = request.POST
        )
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
    else:
        user_form = UserEditForm(instance = request.user)
        profile_form = ProfileEditForm(instance = request.user.profile)
    return render(request, "auctions/edit.html", {
        "user_form": user_form,
        "profile_form": profile_form,
    })