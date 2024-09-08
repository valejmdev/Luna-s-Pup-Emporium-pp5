from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .models import UserProfile
from .forms import UserUpdateForm
from checkout.models import Order


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
            # Update the UserProfile fields
            user_profile.address = request.POST.get('address')
            user_profile.phone_number = request.POST.get('phone_number')
            user_profile.save()

            messages.success(request, 'Your profile has been updated!')
            return redirect('profiles:profile', username=user.username)

        if 'delete' in request.POST:
            user.delete()
            messages.success(request, 'Your profile has been deleted.')
            return redirect('home')

    else:
        u_form = UserUpdateForm(
            instance=user,
            initial={
                'address': user_profile.address,
                'phone_number': user_profile.phone_number,
            }
        )

    # Fetch all orders for the logged-in user
    user_orders = Order.objects.filter(user=user)

    is_edit_mode = request.GET.get('edit') == 'true'

    context = {
        'user': user,
        'u_form': u_form,
        'user_profile': user_profile,
        'user_orders': user_orders,
        'is_edit_mode': is_edit_mode
    }

    return render(request, 'profiles/profile.html', context)
