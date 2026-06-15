"""AI Predictions for Smart Parking System."""
import os, sys
import numpy as np
import datetime

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
sys.path.insert(0, BASE_DIR)

from ai.model import load_model, build_occupancy_model, save_model
from sklearn.preprocessing import StandardScaler


def _ensure_model():
    model, scaler = load_model()
    if model is None:
        # Auto-train with synthetic data if no model exists
        from ai.training import train
        model, scaler = train()
    return model, scaler


def predict_occupancy(hour, day_of_week, month, is_weekend=None, is_holiday=0):
    model, scaler = _ensure_model()
    if is_weekend is None:
        is_weekend = 1 if day_of_week >= 5 else 0
    features = np.array([[hour, day_of_week, month, is_weekend, is_holiday]])
    features_scaled = scaler.transform(features)
    pred = model.predict(features_scaled)[0]
    return round(float(np.clip(pred, 0, 1)), 3)


def get_peak_hours():
    now = datetime.datetime.now()
    dow = now.weekday()
    month = now.month
    hourly = []
    for h in range(24):
        occ = predict_occupancy(h, dow, month)
        hourly.append({'hour': h, 'occupancy': occ})
    peak = sorted(hourly, key=lambda x: x['occupancy'], reverse=True)[:3]
    return [f"{p['hour']:02d}:00" for p in peak], hourly


def get_predictions():
    now = datetime.datetime.now()
    try:
        # Current hour occupancy
        current_occ = predict_occupancy(now.hour, now.weekday(), now.month)

        # Next 12 hours
        next_12 = []
        labels_12 = []
        for i in range(12):
            h = (now.hour + i) % 24
            occ = predict_occupancy(h, now.weekday(), now.month)
            next_12.append(round(occ * 100, 1))
            labels_12.append(f"{h:02d}:00")

        # Find free slot time (first hour < 60% occupancy)
        peak_hours, hourly_all = get_peak_hours()
        free_slot_time = "N/A"
        for entry in hourly_all:
            if entry['hour'] > now.hour and entry['occupancy'] < 0.6:
                free_slot_time = f"{entry['hour']:02d}:00"
                break

        # Full day occupancy for chart
        day_labels = [f"{h:02d}:00" for h in range(24)]
        day_occ = [round(predict_occupancy(h, now.weekday(), now.month) * 100, 1) for h in range(24)]

        return {
            'current_occupancy': round(current_occ * 100, 1),
            'peak_hours': peak_hours,
            'free_slot_time': free_slot_time,
            'next_12_labels': labels_12,
            'next_12_data': next_12,
            'day_labels': day_labels,
            'day_occupancy': day_occ,
            'crowd_level': 'High' if current_occ > 0.7 else 'Medium' if current_occ > 0.4 else 'Low',
        }
    except Exception as e:
        return {
            'current_occupancy': 45.0,
            'peak_hours': ['08:00', '12:00', '17:00'],
            'free_slot_time': '14:00',
            'next_12_labels': [f"{(now.hour+i)%24:02d}:00" for i in range(12)],
            'next_12_data': [45] * 12,
            'day_labels': [f"{h:02d}:00" for h in range(24)],
            'day_occupancy': [30]*8 + [70, 80, 75, 65, 60, 55, 50, 75, 80, 70, 50, 40, 30, 25, 20, 15],
            'crowd_level': 'Medium',
            'error': str(e),
        }
