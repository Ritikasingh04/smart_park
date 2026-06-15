"""
Management command to seed parking slots and demo data.
Run: python manage.py seed_data
"""
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from backend.booking.models import ParkingSlot, Booking, Revenue
from backend.authentication.models import UserProfile
import datetime
import random
import uuid


class Command(BaseCommand):
    help = 'Seed the database with parking slots and demo data'

    def handle(self, *args, **options):
        self.stdout.write('Seeding database...')

        # Create parking slots: 5 rows × 10 slots = 50 total
        rows = ['A', 'B', 'C', 'D', 'E']
        statuses = ['available', 'occupied', 'reserved']
        weights = [0.5, 0.3, 0.2]

        slot_count = 0
        for ri, row in enumerate(rows):
            for pos in range(1, 11):
                slot_num = f"{row}{pos:02d}"
                status = random.choices(statuses, weights)[0]
                slot, created = ParkingSlot.objects.get_or_create(
                    slot_number=slot_num,
                    defaults={
                        'row': row,
                        'position': pos,
                        'status': status,
                        'floor': 1,
                        'grid_x': pos - 1,
                        'grid_y': ri,
                    }
                )
                if created:
                    slot_count += 1
        self.stdout.write(self.style.SUCCESS(f'Created {slot_count} parking slots'))

        # Create demo admin user
        if not User.objects.filter(username='admin').exists():
            admin = User.objects.create_superuser('admin', 'admin@smartparking.com', 'admin123')
            UserProfile.objects.get_or_create(user=admin, defaults={'role': 'admin', 'phone': '9876543210'})
            self.stdout.write(self.style.SUCCESS('Created admin user (admin / admin123)'))

        # Create demo regular user
        if not User.objects.filter(username='user1').exists():
            user = User.objects.create_user('user1', 'user1@example.com', 'user1234',
                                            first_name='Priya', last_name='Sharma')
            UserProfile.objects.get_or_create(user=user, defaults={'role': 'user', 'phone': '9123456789'})
            self.stdout.write(self.style.SUCCESS('Created user (user1 / user1234)'))

        # Seed historical bookings for revenue charts
        user = User.objects.filter(username='user1').first()
        if user:
            slots = list(ParkingSlot.objects.all())
            today = datetime.date.today()
            booking_count = 0
            for days_back in range(30):
                d = today - datetime.timedelta(days=days_back)
                num_bookings = random.randint(2, 12)
                for _ in range(num_bookings):
                    slot = random.choice(slots)
                    dur = random.choice([1, 2, 3, 4])
                    amount = dur * 50
                    ref = uuid.uuid4().hex[:8].upper()
                    b = Booking.objects.create(
                        booking_ref=ref,
                        user=user,
                        slot=slot,
                        name='Demo User',
                        vehicle_number=f'KA{random.randint(10,99)}AB{random.randint(1000,9999)}',
                        booking_date=d,
                        start_time=datetime.time(random.randint(7, 20), 0),
                        duration_hours=dur,
                        status='completed',
                        amount=amount,
                    )
                    Revenue.objects.get_or_create(booking=b, defaults={'amount': amount, 'date': d})
                    booking_count += 1
            self.stdout.write(self.style.SUCCESS(f'Created {booking_count} historical bookings'))

        self.stdout.write(self.style.SUCCESS('Database seeded successfully!'))
        self.stdout.write('')
        self.stdout.write('Login credentials:')
        self.stdout.write('  Admin:  admin / admin123  →  /adminpanel/')
        self.stdout.write('  User:   user1 / user1234  →  /dashboard/')
