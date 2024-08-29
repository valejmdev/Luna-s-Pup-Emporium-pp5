from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .models import UserProfile  
from .forms import UserUpdateForm

@login_required
def profile(request, username):
    user = get_object_or_404(User, username=username)

    # Ensure the user has a UserProfile instance
    try:
        user_profile = user.userprofile
    except UserProfile.DoesNotExist:
        user_profile = UserProfile.objects.create(user=user)

    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=user)
        if 'update' in request.POST and u_form.is_valid():
            u_form.save()
            messages.success(request, 'Your profile has been updated!')
            return redirect('profiles:profile', username=user.username)  # Corrected here

        if 'delete' in request.POST:
            user.delete()
            messages.success(request, 'Your profile has been deleted.')
            return redirect('home')

    else:
        # Ensure the form is populated with existing data
        u_form = UserUpdateForm(
            instance=user,
            initial={
                'address': user_profile.address,
                'phone_number': user_profile.phone_number,
            }
        )

    is_edit_mode = request.GET.get('edit') == 'true'

    context = {
        'user': user,
        'u_form': u_form,
        'is_edit_mode': is_edit_mode
    }

    return render(request, 'profiles/profile.html', context)
