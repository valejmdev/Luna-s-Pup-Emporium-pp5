from allauth.account.forms import SignupForm
from django import forms
from django.contrib.auth.models import User
from .models import UserProfile

class CustomSignupForm(SignupForm):
    address = forms.CharField(max_length=255, required=False)
    phone_number = forms.CharField(max_length=15, required=False)

    def save(self, request):
        user = super(CustomSignupForm, self).save(request)
        print(f"User {user.username} created successfully.")  # Debug message

        # Create or update the UserProfile for the new user
        user_profile, created = UserProfile.objects.get_or_create(user=user)
        
        print(f"Profile created: {created}, updating profile data.")  # Debug message

        # Update the profile fields
        user_profile.address = self.cleaned_data.get('address')
        user_profile.phone_number = self.cleaned_data.get('phone_number')
        user_profile.save()

        print("Profile saved successfully.")  # Debug message
        
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