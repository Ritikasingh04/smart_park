from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from backend.booking.models import Booking

@login_required
def history_view(request):
    bookings = Booking.objects.filter(user=request.user).order_by('-booked_at')
    return render(request, 'history/history.html', {'bookings': bookings})
