from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from allauth.account.adapter import DefaultAccountAdapter
from allauth.socialaccount.models import SocialAccount
from django.shortcuts import redirect
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth import get_user_model

User = get_user_model()

class CustomSocialAccountAdapter(DefaultSocialAccountAdapter):
    def pre_social_login(self, request, sociallogin):
        # If the user is already logged in, do nothing
        if request.user.is_authenticated:
            return
        # Try to find an existing user with the same email
        email = sociallogin.account.extra_data.get('email') or sociallogin.user.email
        if email:
            try:
                user = User.objects.get(email=email)
                # If found, connect this social account to the existing user
                sociallogin.connect(request, user)
            except User.DoesNotExist:
                pass  # No user with this email, proceed as normal
        # Otherwise, proceed as normal
        return super().pre_social_login(request, sociallogin)

    def save_user(self, request, sociallogin, form=None):
        user = super().save_user(request, sociallogin, form)
        # Always set username to email prefix for social logins
        if user.email:
            user.username = user.email.split('@')[0]
            user.save()
        
        # Store user ID in session for later use
        request.session['user_id'] = user.id
        
        # For social logins, always redirect to set password first
        if not sociallogin.is_existing:
            messages.info(request, 'Please set a password for your account.')
            return redirect('set_password')
            
        return user

    def get_connect_redirect_url(self, request, socialaccount):
        """
        Returns the default URL to redirect to after successfully
        connecting a social account.
        """
        return reverse('update_profile')

class CustomAccountAdapter(DefaultAccountAdapter):
    def is_open_for_signup(self, request):
        return True

    def save_user(self, request, user, form, commit=True):
        user = super().save_user(request, user, form, commit=False)
        if form.cleaned_data.get('password1'):
            user.set_password(form.cleaned_data['password1'])
        if commit:
            user.save()
        return user 