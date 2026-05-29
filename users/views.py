from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from .models import Profile
from .forms import CustomRegisterForm, ProfileForm


def register(request):
    if request.method == 'POST':
        form = CustomRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            Profile.objects.get_or_create(user=user)
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            return redirect('users:profile')
    else:
        form = CustomRegisterForm()
    return render(request, 'users/register.html', {'form': form})



@login_required
def profile_view(request):
    user_profile = request.user.profile 
    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=user_profile)
        if form.is_valid():
            form.save()
            return redirect('users:profile')
    else:
        form = ProfileForm(instance=user_profile)
    context = {
        'profile': user_profile,
        'form': form
    }
    return render(request, 'users/profile.html', context)
