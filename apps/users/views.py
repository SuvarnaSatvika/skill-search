from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from .models import Profile
from .forms import ProfileForm
from apps.connections.models import Connection

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.shortcuts import render, redirect

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('search')
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})


@login_required
def search(request):
    skill = request.GET.get('skill', '')
    profiles = []
    if skill:
        profiles = Profile.objects.filter(skills__icontains=skill).exclude(user=request.user)

    # Precompute connections
    profiles_with_conn = []
    for profile in profiles:
        conn = Connection.objects.filter(from_user=request.user, to_user=profile.user).first()
        profiles_with_conn.append({'profile': profile, 'conn': conn})

    context = {
        'skill': skill,
        'profiles_with_conn': profiles_with_conn,
    }
    return render(request, 'users/search.html', context)

@login_required
def edit_profile(request):
    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=request.user.profile)
        if form.is_valid():
            form.save()
            return redirect('search')
    else:
        form = ProfileForm(instance=request.user.profile)
    return render(request, 'users/edit_profile.html', {'form': form})