"""Train the AI model using historical booking data."""
import os, sys, django
import numpy as np

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
sys.path.insert(0, BASE_DIR)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sps.settings')
django.setup()

from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from backend.booking.models import Booking, ParkingSlot
from ai.model import build_occupancy_model, save_model
from django.db.models import Count
from django.utils import timezone
import datetime


def generate_synthetic_data(n_samples=500):
    """Generate synthetic training data based on realistic patterns."""
    np.random.seed(42)
    X, y = [], []
    for _ in range(n_samples):
        hour = np.random.randint(0, 24)
        day_of_week = np.random.randint(0, 7)
        month = np.random.randint(1, 13)
        is_weekend = 1 if day_of_week >= 5 else 0
        is_holiday = 1 if np.random.random() < 0.05 else 0

        # Realistic occupancy patterns
        base = 0.3
        if 8 <= hour <= 10:
            base += 0.4
        elif 11 <= hour <= 14:
            base += 0.3
        elif 17 <= hour <= 19:
            base += 0.35
        elif 0 <= hour <= 6:
            base -= 0.2
        if is_weekend:
            base += 0.1
        if is_holiday:
            base += 0.15
        base = min(max(base + np.random.normal(0, 0.05), 0), 1)
        X.append([hour, day_of_week, month, is_weekend, is_holiday])
        y.append(base)
    return np.array(X), np.array(y)


def train():
    X, y = generate_synthetic_data(1000)

    # Try to augment with real data
    try:
        bookings = Booking.objects.all()
        total_slots = ParkingSlot.objects.count() or 20
        for b in bookings:
            hour = b.start_time.hour
            dow = b.booking_date.weekday()
            month = b.booking_date.month
            is_weekend = 1 if dow >= 5 else 0
            occ = min(1.0, (Booking.objects.filter(
                booking_date=b.booking_date, status='active').count() / total_slots))
            X = np.vstack([X, [hour, dow, month, is_weekend, 0]])
            y = np.append(y, occ)
    except Exception:
        pass

    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.2, random_state=42)

    model = build_occupancy_model()
    model.fit(X_train, y_train)
    score = model.score(X_test, y_test)
    save_model(model, scaler)
    print(f"Model trained. R² score: {score:.4f}")
    return model, scaler


if __name__ == '__main__':
    train()
