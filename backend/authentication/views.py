from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from .models import UserProfile


def landing(request):
    if request.user.is_authenticated:
        try:
            if request.user.profile.is_admin:
                return redirect('adminpanel:dashboard')
        except Exception:
            pass
        return redirect('dashboard:index')
    return render(request, 'landing.html')


def user_login(request):
    if request.user.is_authenticated:
        return redirect('dashboard:index')
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '')
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            try:
                if user.profile.is_admin:
                    return redirect('adminpanel:dashboard')
            except Exception:
                pass
            return redirect('dashboard:index')
        else:
            messages.error(request, 'Invalid username or password.')
    return render(request, 'login.html')


def admin_login(request):
    if request.user.is_authenticated:
        try:
            if request.user.profile.is_admin:
                return redirect('adminpanel:dashboard')
        except Exception:
            pass
        return redirect('dashboard:index')
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '')
        user = authenticate(request, username=username, password=password)
        if user:
            try:
                profile = user.profile
                if profile.is_admin or user.is_superuser:
                    login(request, user)
                    return redirect('adminpanel:dashboard')
                else:
                    messages.error(request, 'You do not have admin privileges.')
            except Exception:
                messages.error(request, 'Admin profile not found.')
        else:
            messages.error(request, 'Invalid admin credentials.')
    return render(request, 'admin_login.html')


def register(request):
    if request.user.is_authenticated:
        return redirect('dashboard:index')
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        email = request.POST.get('email', '').strip()
        password1 = request.POST.get('password1', '')
        password2 = request.POST.get('password2', '')
        first_name = request.POST.get('first_name', '').strip()
        last_name = request.POST.get('last_name', '').strip()

        if not username or not email or not password1:
            messages.error(request, 'All fields are required.')
        elif password1 != password2:
            messages.error(request, 'Passwords do not match.')
        elif User.objects.filter(username=username).exists():
            messages.error(request, 'Username already taken.')
        elif User.objects.filter(email=email).exists():
            messages.error(request, 'Email already registered.')
        elif len(password1) < 8:
            messages.error(request, 'Password must be at least 8 characters.')
        else:
            user = User.objects.create_user(
                username=username, email=email,
                password=password1,
                first_name=first_name, last_name=last_name
            )
            UserProfile.objects.get_or_create(user=user, defaults={'role': 'user'})
            login(request, user)
            messages.success(request, f'Welcome, {user.first_name or user.username}!')
            return redirect('dashboard:index')
    return render(request, 'register.html')


def user_logout(request):
    logout(request)
    return redirect('landing')
