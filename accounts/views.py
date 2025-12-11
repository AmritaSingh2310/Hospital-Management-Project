from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import RegisterForm, AuthenticationForm
from .models import UserProfile

def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            profile = UserProfile.objects.create(
                user=user, 
                role=form.cleaned_data['role']
            )
            login(request, user)
            messages.success(request, 'Registration successful!')
            if profile.role == 'doctor':
                return redirect('doctor_dashboard')
            return redirect('patient_dashboard')
    else:
        form = RegisterForm()
    return render(request, 'accounts/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            try:
                profile = UserProfile.objects.get(user=user)
                if profile.role == 'doctor':
                    return redirect('doctor_dashboard')
            except UserProfile.DoesNotExist:
                pass
            return redirect('patient_dashboard')
    else:
        form = AuthenticationForm()
    return render(request, 'accounts/login.html', {'form': form})

@login_required
def doctor_dashboard(request):
    profile = UserProfile.objects.get(user=request.user)
    return render(request, 'accounts/doctor_dashboard.html', {'profile': profile})

@login_required
def patient_dashboard(request):
    profile = UserProfile.objects.get(user=request.user)
    return render(request, 'accounts/patient_dashboard.html', {'profile': profile})

def logout_view(request):
    logout(request)
    messages.success(request, 'Logged out successfully!')
    return redirect('login')
