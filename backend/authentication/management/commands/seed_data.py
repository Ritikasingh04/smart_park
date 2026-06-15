import os, sys
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from backend.authentication.models import UserProfile
from backend.booking.models import ParkingSlot, Booking, Revenue
from django.utils import timezone
import datetime, random


class Command(BaseCommand):
    help = 'Seed the database with initial parking slots and demo accounts'

    def handle(self, *args, **options):
        # --- Parking Slots ---
        rows = ['A', 'B', 'C', 'D', 'E']
        created = 0
        for row_idx, row in enumerate(rows):
            for pos in range(1, 11):
                slot_num = f"{row}{pos:02d}"
                _, made = ParkingSlot.objects.get_or_create(
                    slot_number=slot_num,
                    defaults={'row': row, 'position': pos,
                              'grid_x': pos-1, 'grid_y': row_idx, 'status': 'available', 'floor': 1})
                if made:
                    created += 1
        self.stdout.write(self.style.SUCCESS(f'Parking slots ready ({created} new, 50 total).'))

        # --- Admin User ---
        if not User.objects.filter(username='admin').exists():
            adm = User.objects.create_superuser('admin', 'admin@sps.com', 'admin123',
                                                first_name='System', last_name='Admin')
            UserProfile.objects.get_or_create(user=adm, defaults={'role': 'admin'})
            self.stdout.write(self.style.SUCCESS('Admin: admin / admin123'))
        else:
            adm = User.objects.get(username='admin')
            p, _ = UserProfile.objects.get_or_create(user=adm, defaults={'role': 'admin'})
            if p.role != 'admin':
                p.role = 'admin'; p.save()
            self.stdout.write('Admin user already exists.')

        # --- Demo User ---
        if not User.objects.filter(username='demo').exists():
            demo = User.objects.create_user('demo', 'demo@sps.com', 'demo1234',
                                            first_name='Demo', last_name='Driver')
            UserProfile.objects.get_or_create(user=demo, defaults={'role': 'user', 'phone': '9876543210'})
            self.stdout.write(self.style.SUCCESS('Demo user: demo / demo1234'))

        # --- Sample Bookings ---
        demo_user = User.objects.filter(username='demo').first()
        if demo_user and Revenue.objects.count() == 0:
            slots_list = list(ParkingSlot.objects.all()[:20])
            today = timezone.now().date()
            for i in range(25):
                bdate = today - datetime.timedelta(days=random.randint(0, 45))
                slot  = random.choice(slots_list)
                dur   = random.choice([1, 2, 3, 4, 6])
                amt   = dur * 50
                stat  = random.choice(['completed','completed','completed','cancelled'])
                b = Booking.objects.create(
                    user=demo_user, slot=slot, name='Demo Driver',
                    vehicle_number=f'KA{random.randint(1,9):02d}AB{random.randint(1000,9999)}',
                    booking_date=bdate,
                    start_time=datetime.time(random.randint(7, 21), 0),
                    duration_hours=dur, status=stat, amount=amt)
                Revenue.objects.get_or_create(booking=b, defaults={'amount': amt, 'date': bdate})

            # Random slot statuses for visual variety
            all_slots = list(ParkingSlot.objects.all())
            for s in all_slots:
                s.status = random.choices(['available','occupied','reserved'], weights=[6,2,2])[0]
                s.save()
            self.stdout.write(self.style.SUCCESS('Sample data seeded.'))

        # --- Train AI ---
        try:
            import sys, os
            sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(
                os.path.dirname(os.path.dirname(os.path.dirname(__file__)))))))
            from ai.training import train
            train()
            self.stdout.write(self.style.SUCCESS('AI model trained.'))
        except Exception as e:
            self.stdout.write(self.style.WARNING(f'AI training note: {e}'))

        self.stdout.write(self.style.SUCCESS('\n✅ Setup complete!'))
        self.stdout.write('  Admin : admin / admin123')
        self.stdout.write('  User  : demo  / demo1234')
