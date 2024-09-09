from django import forms
from django.core.exceptions import ValidationError
from django.core.validators import EmailValidator
from django.contrib.auth.models import User
from allauth.account.forms import SignupForm
from .models import UserProfile

class CustomSignupForm(SignupForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Custom error messages for fields
        self.fields['username'].error_messages = {
            'required': 'Username is required.',
            'min_length': 'Username must be at least 3 characters long.',
            'max_length': 'Username cannot exceed 25 characters.'
        }
        self.fields['email'].error_messages = {
            'required': 'Email is required.',
            'invalid': 'Enter a valid email address.'
        }
        self.fields['password1'].error_messages = {
            'required': 'Password is required.',
        }
        self.fields['password2'].error_messages = {
            'required': 'Password confirmation is required.',
            'password_mismatch': 'Passwords do not match.',
        }

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if len(username) < 3:
            raise ValidationError('Username must be at least 3 characters long.')
        if len(username) > 25:
            raise ValidationError('Username cannot exceed 25 characters.')
        return username

    def clean_email(self):
        email = self.cleaned_data.get('email')
        validator = EmailValidator()
        try:
            validator(email)
        except ValidationError:
            raise ValidationError('Enter a valid email address.')
        return email

    def save(self, request):
        if not self.is_valid():
            print(f"Form errors: {self.errors}")
            return None
        
        user = super(CustomSignupForm, self).save(request)
        
        if user:
            print(f"User {user.username} created successfully.")
        else:
            print(f"Form errors after save: {self.errors}")

        # Create or update the UserProfile for the new user
        user_profile, created = UserProfile.objects.get_or_create(user=user)
        user_profile.save()

        return user

class UserUpdateForm(forms.ModelForm):
    address = forms.CharField(max_length=255, required=False)
    phone_number = forms.CharField(max_length=15, required=False)

    class Meta:
        model = User
        fields = ['username', 'email', 'address', 'phone_number']

    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()
            user_profile, created = UserProfile.objects.get_or_create(user=user)
            user_profile.address = self.cleaned_data.get('address')
            user_profile.phone_number = self.cleaned_data.get('phone_number')
            user_profile.save()
        return user