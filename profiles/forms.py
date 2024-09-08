from django import forms
from django.contrib.auth.models import User
from .models import UserProfile


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
            user_profile, created = UserProfile.objects.get_or_create(
                user=user
            )
            user_profile.address = self.cleaned_data.get('address')
            user_profile.phone_number = self.cleaned_data.get('phone_number')
            user_profile.save()
        return user
