from django.shortcuts import render, redirect
from django.contrib.auth import logout, update_session_auth_hash
from django.contrib.auth import get_user_model
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import SetPasswordForm, AuthenticationForm, UserCreationForm
from .forms import ProfileUpdateForm
from django.contrib.auth import authenticate, login
from django.conf import settings
from allauth.socialaccount.models import SocialAccount

User = get_user_model()

# Create your views here.
def home(request):
    login_form = AuthenticationForm()
    register_form = UserCreationForm()
    social_accounts = []
    current_provider = None
    if request.user.is_authenticated:
        social_accounts = SocialAccount.objects.filter(user=request.user)
        if hasattr(request.user, 'socialaccount_set'):
            last_login = request.user.socialaccount_set.order_by('-last_login').first()
            if last_login:
                current_provider = last_login.provider
    return render(request, "users/home.html", {
        "login_form": login_form,
        "register_form": register_form,
        "social_accounts": social_accounts,
        "current_provider": current_provider
    })

def login_view(request):
    if request.user.is_authenticated:
        return redirect("home")
    form = AuthenticationForm(request, data=request.POST or None)
    if request.method == "POST":
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, f"Successfully signed in as {user.username}.")
            return redirect("home")
        else:
            messages.error(request, "Invalid username or password.")
    return render(request, "users/login.html", {"form": form})

def register_view(request):
    if request.user.is_authenticated:
        return redirect("home")
    form = UserCreationForm(request.POST or None)
    if request.method == "POST":
        if form.is_valid():
            user = form.save()
            user.backend = settings.AUTHENTICATION_BACKENDS[0]  # Specify backend
            login(request, user)
            messages.success(request, f"Successfully registered and signed in as {user.username}.")
            return redirect("home")
        else:
            messages.error(request, "Please correct the errors below.")
    return render(request, "users/register.html", {"form": form})

def logout_view(request):
    logout(request)
    messages.success(request, "You have been logged out successfully.")
    return redirect("home")

@login_required
def set_password(request):
    if request.method == "POST":
        form = SetPasswordForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Keep the user logged in
            messages.success(request, "Your password has been set successfully.")
            messages.info(request, "Please complete your profile information.")
            return redirect('update_profile')
    else:
        form = SetPasswordForm(request.user)
    return render(request, "users/set_password.html", {"form": form})

@login_required
def update_profile(request):
    user = request.user
    auto_generated = False
    # Consider username auto-generated if it matches email or its prefix
    if user.username == user.email or user.username == user.email.split('@')[0]:
        auto_generated = True
    if request.method == "POST":
        form = ProfileUpdateForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, "Your profile has been updated successfully.")
            return redirect("home")
    else:
        form = ProfileUpdateForm(instance=user)
    return render(request, "users/update_profile.html", {"form": form, "auto_generated": auto_generated})

@login_required
def post_login_redirect(request):
    user = request.user
    if not user.has_usable_password():
        return redirect('set_password')
    if not user.first_name or not user.last_name:
        return redirect('update_profile')
    return redirect('home')   



