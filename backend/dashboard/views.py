from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from backend.booking.models import ParkingSlot, Booking
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
from ai.prediction import get_predictions


@login_required
def index(request):
    # Redirect admin
    try:
        if request.user.profile.is_admin:
            return redirect('adminpanel:dashboard')
    except Exception:
        pass

    slots = ParkingSlot.objects.all()
    total = slots.count()
    available = slots.filter(status='available').count()
    occupied = slots.filter(status='occupied').count()
    reserved = slots.filter(status='reserved').count()

    my_active = Booking.objects.filter(user=request.user, status='active').first()
    recent_bookings = Booking.objects.filter(user=request.user).order_by('-booked_at')[:5]

    # AI Predictions
    predictions = get_predictions()

    context = {
        'total_slots': total,
        'available_slots': available,
        'occupied_slots': occupied,
        'reserved_slots': reserved,
        'my_active_booking': my_active,
        'recent_bookings': recent_bookings,
        'predictions': predictions,
        'slots': slots,
    }
    return render(request, 'dashboard/dashboard.html', context)
