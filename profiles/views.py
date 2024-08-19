from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login as auth_login
from django.contrib.auth.forms import AuthenticationForm
from .forms import UserRegisterForm, UserUpdateForm

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
def profile(request):
    """
    View to handle both viewing and updating the user profile.
    """
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        if 'update' in request.POST and u_form.is_valid():
            u_form.save()
            messages.success(request, 'Your profile has been updated!')
            return redirect('profile')

        if 'delete' in request.POST:
            request.user.delete()
            messages.success(request, 'Your profile has been deleted.')
            return redirect('home')

    else:
        u_form = UserUpdateForm(instance=request.user)

    is_edit_mode = request.GET.get('edit') == 'true'

    context = {
        'user': request.user,
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
    """
    Handle user logout.
    """
    from django.contrib.auth import logout as auth_logout
    auth_logout(request)
    messages.success(request, 'You have been logged out.')
    return redirect('login')

def newsletter(request):
    return render(request, 'profiles/newsletter.html')

def terms_conditions(request):
    return render(request, 'profiles/terms_conditions.html')