from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.utils import timezone
from django.http import JsonResponse
from django.db.models import Sum, Count
from backend.booking.models import ParkingSlot, Booking, Revenue
import datetime
import json


def admin_required(func):
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('admin_login')
        try:
            if not (request.user.profile.is_admin or request.user.is_superuser):
                messages.error(request, 'Admin access required.')
                return redirect('dashboard:index')
        except Exception:
            messages.error(request, 'Admin access required.')
            return redirect('dashboard:index')
        return func(request, *args, **kwargs)
    wrapper.__name__ = func.__name__
    return wrapper


@admin_required
def dashboard(request):
    slots = ParkingSlot.objects.all()
    total = slots.count()
    available = slots.filter(status='available').count()
    occupied = slots.filter(status='occupied').count()
    reserved = slots.filter(status='reserved').count()

    today = timezone.now().date()
    total_revenue = Revenue.objects.aggregate(t=Sum('amount'))['t'] or 0
    today_revenue = Revenue.objects.filter(date=today).aggregate(t=Sum('amount'))['t'] or 0
    total_bookings = Booking.objects.count()
    active_bookings = Booking.objects.filter(status='active').count()

    # Chart data - last 7 days revenue
    days, rev_data = [], []
    for i in range(6, -1, -1):
        d = today - datetime.timedelta(days=i)
        rev = Revenue.objects.filter(date=d).aggregate(t=Sum('amount'))['t'] or 0
        days.append(d.strftime('%b %d'))
        rev_data.append(float(rev))

    # Monthly revenue
    months, monthly_rev = [], []
    for i in range(5, -1, -1):
        if today.month - i <= 0:
            month_num = today.month - i + 12
            year = today.year - 1
        else:
            month_num = today.month - i
            year = today.year
        rev = Revenue.objects.filter(date__month=month_num, date__year=year).aggregate(t=Sum('amount'))['t'] or 0
        months.append(datetime.date(year, month_num, 1).strftime('%b %Y'))
        monthly_rev.append(float(rev))

    # Booking trends last 7 days
    booking_trends = []
    for i in range(6, -1, -1):
        d = today - datetime.timedelta(days=i)
        cnt = Booking.objects.filter(booked_at__date=d).count()
        booking_trends.append(cnt)

    context = {
        'total_slots': total, 'available_slots': available,
        'occupied_slots': occupied, 'reserved_slots': reserved,
        'total_revenue': total_revenue, 'today_revenue': today_revenue,
        'total_bookings': total_bookings, 'active_bookings': active_bookings,
        'chart_days': json.dumps(days),
        'chart_rev': json.dumps(rev_data),
        'chart_months': json.dumps(months),
        'chart_monthly_rev': json.dumps(monthly_rev),
        'chart_booking_trends': json.dumps(booking_trends),
        'occupancy_pct': round((occupied + reserved) / total * 100, 1) if total else 0,
    }
    return render(request, 'adminpanel/dashboard.html', context)


@admin_required
def slots_view(request):
    slots = ParkingSlot.objects.all().order_by('row', 'position')
    if request.method == 'POST':
        slot_id = request.POST.get('slot_id')
        new_status = request.POST.get('status')
        if slot_id and new_status in ['available', 'occupied', 'reserved']:
            slot = get_object_or_404(ParkingSlot, id=slot_id)
            old_status = slot.status
            slot.status = new_status
            slot.save()
            if old_status == 'reserved' and new_status == 'available':
                Booking.objects.filter(slot=slot, status='active').update(status='completed')
            messages.success(request, f'Slot {slot.slot_number} updated to {new_status}.')
        return redirect('adminpanel:slots')
    return render(request, 'adminpanel/slots.html', {'slots': slots})


@admin_required
def users_view(request):
    users = User.objects.select_related('profile').all().order_by('date_joined')
    return render(request, 'adminpanel/users.html', {'users': users})


@admin_required
def bookings_view(request):
    bookings = Booking.objects.select_related('user', 'slot').all().order_by('-booked_at')
    return render(request, 'adminpanel/bookings.html', {'bookings': bookings})


@admin_required
def revenue_view(request):
    revenues = Revenue.objects.select_related('booking__user', 'booking__slot').all().order_by('-created_at')
    total = revenues.aggregate(t=Sum('amount'))['t'] or 0
    return render(request, 'adminpanel/revenue.html', {'revenues': revenues, 'total': total})
