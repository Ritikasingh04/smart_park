#!/bin/bash
echo "============================================"
echo " Smart Parking System - Setup Script"
echo "============================================"

# Use python3 explicitly
PYTHON=python3
$PYTHON --version 2>/dev/null || { echo "ERROR: python3 not found."; exit 1; }

echo "Step 1: Creating virtual environment..."
$PYTHON -m venv venv

echo "Step 2: Activating virtual environment..."
source venv/bin/activate

echo "Step 3: Installing requirements..."
pip install -r requirements.txt

echo "Step 4: Running migrations..."
python manage.py migrate

echo "Step 5: Seeding database..."
python manage.py seed_data

echo ""
echo "============================================"
echo " SETUP COMPLETE!"
echo "============================================"
echo " Admin Login : admin / admin123"
echo " User  Login : demo  / demo1234"
echo " Open: http://127.0.0.1:8000"
echo ""
python manage.py runserver
