from django import forms
from django.contrib.auth.password_validation import validate_password


class CustomAuthenticationForm(forms.Form):
    username = forms.CharField(min_length=1, max_length=150)
    password = forms.CharField(widget=forms.PasswordInput())
