from django import forms
from django.contrib.auth.models import User
from .models import UserProfile

class UserRegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    address = forms.CharField(max_length=255, required=False)
    phone_number = forms.CharField(max_length=15, required=False)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'address', 'phone_number']

    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()
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
            # Corrected the reference from user.profile to user.userprofile
            user_profile = UserProfile.objects.get(user=user)
            user_profile.address = self.cleaned_data.get('address')
            user_profile.phone_number = self.cleaned_data.get('phone_number')
            user_profile.save()
        return user