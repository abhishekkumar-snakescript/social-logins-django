from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserChangeForm

User = get_user_model()

class ProfileUpdateForm(UserChangeForm):
    password = None  # Remove password field from the form
    
    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name')
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
        } 