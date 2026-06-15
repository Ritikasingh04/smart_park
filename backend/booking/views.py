from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from django.http import JsonResponse
from .models import ParkingSlot, Booking, Revenue
import datetime


@login_required
def booking_index(request):
    slots = ParkingSlot.objects.all().order_by('row', 'position')
    user_active = Booking.objects.filter(user=request.user, status='active').first()

    if request.method == 'POST':
        slot_id = request.POST.get('slot_id')
        name = request.POST.get('name', '').strip()
        vehicle_number = request.POST.get('vehicle_number', '').strip()
        booking_date = request.POST.get('booking_date', '')
        start_time = request.POST.get('start_time', '')
        duration = request.POST.get('duration', '1')

        if not all([slot_id, name, vehicle_number, booking_date, start_time]):
            messages.error(request, 'All fields are required.')
        else:
            try:
                slot = ParkingSlot.objects.get(id=slot_id, status='available')
                dur = float(duration)
                bdate = datetime.date.fromisoformat(booking_date)
                stime = datetime.time.fromisoformat(start_time)
                start_dt = timezone.make_aware(datetime.datetime.combine(bdate, stime))
                expires_dt = start_dt + datetime.timedelta(hours=dur)
                amount = round(dur * 50, 2)

                booking = Booking.objects.create(
                    user=request.user,
                    slot=slot,
                    name=name,
                    vehicle_number=vehicle_number,
                    booking_date=bdate,
                    start_time=stime,
                    duration_hours=dur,
                    expires_at=expires_dt,
                    amount=amount,
                )
                slot.status = 'reserved'
                slot.save()
                Revenue.objects.create(booking=booking, amount=amount, date=bdate)
                messages.success(request, f'Slot {slot.slot_number} reserved! Ref: {booking.booking_ref}')
                return redirect('booking:my_bookings')
            except ParkingSlot.DoesNotExist:
                messages.error(request, 'Slot not available.')
            except Exception as e:
                messages.error(request, f'Error: {e}')

    context = {
        'slots': slots,
        'user_active': user_active,
        'today': timezone.now().date().isoformat(),
    }
    return render(request, 'booking/booking.html', context)


@login_required
def my_bookings(request):
    bookings = Booking.objects.filter(user=request.user).order_by('-booked_at')
    return render(request, 'booking/my_bookings.html', {'bookings': bookings})


@login_required
def cancel_booking(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id, user=request.user, status='active')
    booking.status = 'cancelled'
    booking.cancelled_at = timezone.now()
    booking.save()
    booking.slot.status = 'available'
    booking.slot.save()
    messages.success(request, f'Booking {booking.booking_ref} cancelled.')
    return redirect('booking:my_bookings')


@login_required
def slot_status_api(request):
    slots = ParkingSlot.objects.all().values('id', 'slot_number', 'row', 'position', 'status', 'grid_x', 'grid_y')
    return JsonResponse({'slots': list(slots)})
