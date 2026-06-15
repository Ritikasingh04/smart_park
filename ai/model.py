"""AI Model definitions for Smart Parking System."""
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.preprocessing import StandardScaler
import numpy as np
import pickle
import os

MODEL_DIR = os.path.dirname(__file__)
MODEL_PATH = os.path.join(MODEL_DIR, 'trained_model.pkl')
SCALER_PATH = os.path.join(MODEL_DIR, 'scaler.pkl')


def build_occupancy_model():
    return RandomForestRegressor(n_estimators=100, random_state=42, max_depth=6)


def build_peak_model():
    return GradientBoostingRegressor(n_estimators=50, random_state=42)


def save_model(model, scaler):
    with open(MODEL_PATH, 'wb') as f:
        pickle.dump(model, f)
    with open(SCALER_PATH, 'wb') as f:
        pickle.dump(scaler, f)


def load_model():
    if os.path.exists(MODEL_PATH) and os.path.exists(SCALER_PATH):
        with open(MODEL_PATH, 'rb') as f:
            model = pickle.load(f)
        with open(SCALER_PATH, 'rb') as f:
            scaler = pickle.load(f)
        return model, scaler
    return None, None
