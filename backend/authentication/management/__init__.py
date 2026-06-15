import os
import sys

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
sys.path.insert(0, BASE_DIR)

from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from backend.authentication.models import UserProfile
from backend.booking.models import ParkingSlot, Booking, Revenue
from django.utils import timezone
import datetime
import random


class Command(BaseCommand):
    help = 'Seed the database with initial data'

    def add_arguments(self, parser):
        parser.add_argument('--reset', action='store_true', help='Reset all data before seeding')

    def handle(self, *args, **options):
        if options['reset']:
            ParkingSlot.objects.all().delete()
            self.stdout.write('Cleared existing slots.')

        # Create parking slots: 5 rows (A-E), 10 slots each = 50 total
        rows = ['A', 'B', 'C', 'D', 'E']
        slots_per_row = 10
        created = 0

        for row_idx, row in enumerate(rows):
            for pos in range(1, slots_per_row + 1):
                slot_num = f"{row}{pos:02d}"
                slot, made = ParkingSlot.objects.get_or_create(
                    slot_number=slot_num,
                    defaults={
                        'row': row,
                        'position': pos,
                        'grid_x': pos - 1,
                        'grid_y': row_idx,
                        'status': 'available',
                        'floor': 1,
                    }
                )
                if made:
                    created += 1

        self.stdout.write(self.style.SUCCESS(f'Created {created} parking slots (50 total).'))

        # Create admin user
        if not User.objects.filter(username='admin').exists():
            admin = User.objects.create_superuser(
                username='admin',
                email='admin@smartparking.com',
                password='admin123',
                first_name='Admin',
                last_name='User'
            )
            UserProfile.objects.get_or_create(user=admin, defaults={'role': 'admin'})
            self.stdout.write(self.style.SUCCESS('Admin created: username=admin, password=admin123'))
        else:
            admin = User.objects.get(username='admin')
            profile, _ = UserProfile.objects.get_or_create(user=admin, defaults={'role': 'admin'})
            if profile.role != 'admin':
                profile.role = 'admin'
                profile.save()
            self.stdout.write('Admin user already exists.')

        # Create demo user
        if not User.objects.filter(username='demo').exists():
            demo = User.objects.create_user(
                username='demo',
                email='demo@smartparking.com',
                password='demo1234',
                first_name='Demo',
                last_name='Driver'
            )
            UserProfile.objects.get_or_create(user=demo, defaults={'role': 'user', 'phone': '9876543210'})
            self.stdout.write(self.style.SUCCESS('Demo user created: username=demo, password=demo1234'))

        # Seed some sample bookings for charts
        demo_user = User.objects.filter(username='demo').first()
        if demo_user and Revenue.objects.count() == 0:
            slots_list = list(ParkingSlot.objects.all()[:15])
            today = timezone.now().date()

            for i in range(20):
                bdate = today - datetime.timedelta(days=random.randint(0, 30))
                slot = random.choice(slots_list)
                dur = random.choice([1, 2, 3, 4])
                amt = dur * 50
                b = Booking.objects.create(
                    user=demo_user,
                    slot=slot,
                    name='Demo Driver',
                    vehicle_number=f'KA0{random.randint(1,9)}AB{random.randint(1000,9999)}',
                    booking_date=bdate,
                    start_time=datetime.time(random.randint(8, 20), 0),
                    duration_hours=dur,
                    status=random.choice(['completed', 'completed', 'cancelled']),
                    amount=amt,
                )
                Revenue.objects.get_or_create(booking=b, defaults={'amount': amt, 'date': bdate})

            # Mark a few slots as occupied for visual demo
            for slot in ParkingSlot.objects.all()[:8]:
                slot.status = random.choice(['occupied', 'reserved', 'available', 'available'])
                slot.save()

            self.stdout.write(self.style.SUCCESS('Sample bookings and revenue data created.'))

        # Train AI model
        try:
            from ai.training import train
            train()
            self.stdout.write(self.style.SUCCESS('AI model trained successfully.'))
        except Exception as e:
            self.stdout.write(self.style.WARNING(f'AI training skipped: {e}'))

        self.stdout.write(self.style.SUCCESS('\n=== Setup Complete ==='))
        self.stdout.write('Admin login : username=admin  password=admin123')
        self.stdout.write('Demo login  : username=demo   password=demo1234')
        self.stdout.write('Run: python manage.py runserver')
