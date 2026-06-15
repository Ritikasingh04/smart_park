from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from backend.booking.models import ParkingSlot, Booking


@login_required
def map_view(request):
    slots = ParkingSlot.objects.all().order_by('row', 'position')
    my_active = Booking.objects.filter(user=request.user, status='active').first()
    context = {
        'slots': slots,
        'my_active_booking': my_active,
    }
    return render(request, 'map/map.html', context)
