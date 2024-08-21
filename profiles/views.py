from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .models import UserProfile  
from .forms import UserUpdateForm
from django.contrib.auth import logout as auth_logout

def register(request):
    """
    Handle user registration.
    """
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Thank you for creating an account, {username}.')
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'profiles/register.html', {'form': form})

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
            return redirect('profile:profile', username=user.username)

        if 'delete' in request.POST:
            user.delete()
            messages.success(request, 'Your profile has been deleted.')
            return redirect('home')

    else:
        # Here, ensure that the form is populated with existing data
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

def login(request):
    """
    Handle user login.
    """
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            auth_login(request, user)
            messages.success(request, 'You are now logged in.')
            return redirect('profile')
    else:
        form = AuthenticationForm()

    return render(request, 'profiles/login.html', {'form': form})

def logout(request):
    auth_logout(request)
    return redirect('store/index.html')

def newsletter(request):
    return render(request, 'profiles/newsletter.html')

def terms_conditions(request):
    return render(request, 'profiles/terms_conditions.html')