from django import forms
from django.contrib.auth import get_user_model
from .models import Profile
# Form validation for Bid

class RegistrationForm(forms.ModelForm):
    password = forms.CharField(
        label="Password", widget=forms.PasswordInput
    )

    password_confirm = forms.CharField(
        label="Repeat password", widget=forms.PasswordInput
    )

    class Meta:
        model = get_user_model()
        fields = ["username", "first_name", "last_name", "email"]

    def clean_validate_password(self):
        cd = self.cleaned_data
        if cd["password"] != cd["password_confirm"]:
            raise forms.ValidationError("Password don't match.")
        return cd["password_confirm"]


# ALLOW USER TO EDIT PROFILE
class UserEditForm(forms.ModelForm):
    class Meta:
        model = get_user_model()
        fields = ["first_name", "last_name", "email"]

class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ["date_of_birth"]