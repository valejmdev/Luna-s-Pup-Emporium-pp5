from allauth.account.forms import SignupForm
from django import forms
from django.contrib.auth.models import User
from .models import UserProfile

class CustomSignupForm(SignupForm):
    address = forms.CharField(max_length=255, required=False)
    phone_number = forms.CharField(max_length=15, required=False)

    def save(self, request):
        # Save the base SignupForm first (which handles the creation of the User)
        user = super(CustomSignupForm, self).save(request)

        # Create the UserProfile for the user
        UserProfile.objects.create(
            user=user,
            address=self.cleaned_data.get('address'),
            phone_number=self.cleaned_data.get('phone_number')
        )

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
            # Ensure the user profile is updated with new data
            user_profile, created = UserProfile.objects.get_or_create(user=user)
            user_profile.address = self.cleaned_data.get('address')
            user_profile.phone_number = self.cleaned_data.get('phone_number')
            user_profile.save()
        return user