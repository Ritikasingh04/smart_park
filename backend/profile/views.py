from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User


@login_required
def profile_view(request):
    if request.method == 'POST':
        user = request.user
        user.first_name = request.POST.get('first_name', '').strip()
        user.last_name = request.POST.get('last_name', '').strip()
        user.email = request.POST.get('email', '').strip()
        user.save()
        try:
            profile = user.profile
            profile.phone = request.POST.get('phone', '').strip()
            profile.address = request.POST.get('address', '').strip()
            profile.save()
        except Exception:
            pass
        messages.success(request, 'Profile updated successfully!')
        return redirect('userprofile:index')
    return render(request, 'profile/profile.html', {'user': request.user})
