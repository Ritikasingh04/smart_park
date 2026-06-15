from django.db import models
from django.contrib.auth.models import User
import uuid
from django.utils import timezone


class ParkingSlot(models.Model):
    STATUS_CHOICES = [
        ('available', 'Available'),
        ('occupied', 'Occupied'),
        ('reserved', 'Reserved'),
    ]
    slot_number = models.CharField(max_length=10, unique=True)
    row = models.CharField(max_length=5, default='A')
    position = models.IntegerField(default=1)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='available')
    floor = models.IntegerField(default=1)
    # Grid position for map display
    grid_x = models.IntegerField(default=0)
    grid_y = models.IntegerField(default=0)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['row', 'position']

    def __str__(self):
        return f"Slot {self.slot_number} ({self.status})"

    @property
    def status_color(self):
        return {'available': '#22c55e', 'occupied': '#ef4444', 'reserved': '#eab308'}.get(self.status, '#gray')


class Booking(models.Model):
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]
    booking_ref = models.CharField(max_length=12, unique=True, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bookings')
    slot = models.ForeignKey(ParkingSlot, on_delete=models.CASCADE, related_name='bookings')
    name = models.CharField(max_length=100, default='')
    vehicle_number = models.CharField(max_length=20)
    booking_date = models.DateField(default=timezone.now)
    start_time = models.TimeField(default='09:00')
    duration_hours = models.FloatField(default=1.0)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')
    booked_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField(null=True, blank=True)
    cancelled_at = models.DateTimeField(null=True, blank=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    notes = models.TextField(blank=True)

    class Meta:
        ordering = ['-booked_at']

    def save(self, *args, **kwargs):
        if not self.booking_ref:
            self.booking_ref = uuid.uuid4().hex[:8].upper()
        if not self.amount:
            self.amount = round(self.duration_hours * 50, 2)  # ₹50/hr
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Booking {self.booking_ref} — Slot {self.slot.slot_number}"


class Revenue(models.Model):
    booking = models.OneToOneField(Booking, on_delete=models.CASCADE, related_name='revenue')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField(auto_now_add=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Revenue ₹{self.amount} for {self.booking.booking_ref}"


class PredictionRecord(models.Model):
    predicted_at = models.DateTimeField(auto_now_add=True)
    hour = models.IntegerField()
    predicted_occupancy = models.FloatField()
    actual_occupancy = models.FloatField(null=True, blank=True)
    peak_hours = models.JSONField(default=list)
    free_slot_time = models.CharField(max_length=50, blank=True)

    class Meta:
        ordering = ['-predicted_at']
