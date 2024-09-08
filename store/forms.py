from django import forms
from allauth.account.forms import SignupForm
from .models import NewsletterSubscriber
from .models import Review
from profiles.models import UserProfile

class CustomSignupForm(SignupForm):
    address = forms.CharField(max_length=255, required=False)
    phone_number = forms.CharField(max_length=15, required=False)

    def save(self, request):
        user = super(CustomSignupForm, self).save(request)
        print(f"User {user.username} created successfully.")

        # Create or update the UserProfile for the new user
        user_profile, created = UserProfile.objects.get_or_create(
            user=user
        )

        # Update the profile fields
        user_profile.address = self.cleaned_data.get('address')
        user_profile.phone_number = self.cleaned_data.get('phone_number')
        user_profile.save()

        return user

class NewsletterForm(forms.ModelForm):
    class Meta:
        model = NewsletterSubscriber
        fields = ['email']


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'comment']
        widgets = {
            'rating': forms.RadioSelect(
                choices=[(i, str(i)) for i in range(1, 6)]
            ),
            'comment': forms.Textarea(attrs={'rows': 4}),
        }
