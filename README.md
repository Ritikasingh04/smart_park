# 🅿 Smart Parking System

<p align="center">
  <img src="screenshots/Screenshot%202026-06-17%20203855.png" width="900">
</p>

AI-Powered Parking Management System built with Django, SQLite, Scikit-learn, and Chart.js.

---

## 🚀 Quick Setup in VS Code (Step-by-Step)

### Prerequisites
- Python 3.10, 3.11, or 3.12 installed
- VS Code installed
- Git (optional)

---

### Step 1: Open in VS Code

1. **Extract** the `smart_parking_system` ZIP file to a folder (e.g. `C:\Projects\`)
2. Open **VS Code**
3. Click **File → Open Folder** → select `smart_parking_system`

---

### Step 2: Select the Right Python Version

> ⚠️ You have 3 Python versions installed. We'll make sure to use the correct one.

1. Press `Ctrl+Shift+P` → type **"Python: Select Interpreter"**
2. Choose **Python 3.10+** (avoid 2.x)
3. If unsure which to pick, open the VS Code terminal and run:
   ```
   py -0   (Windows — lists all Python versions)
   ```

---

### Step 3: Open the Terminal

Press `` Ctrl+` `` to open the VS Code integrated terminal.

---

### Step 4: Create a Virtual Environment

> This isolates the project's packages from your other Python installations.

**Windows:**
```bash
py -3.11 -m venv venv
venv\Scripts\activate
```

**Mac/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

You should see `(venv)` at the start of your terminal prompt.

---

### Step 5: Install Requirements

```bash
pip install -r requirements.txt
```

This installs: Django, scikit-learn, numpy, Pillow.

---

### Step 6: Set Up the Database

```bash
python manage.py migrate
```

---

### Step 7: Seed Demo Data + Train AI Model

```bash
python manage.py seed_data
```

This creates:
- **50 parking slots** (Rows A–E, 10 slots each)
- **Admin account**: `admin` / `admin123`
- **Demo user account**: `demo` / `demo1234`
- **Sample booking history** (for charts)
- **Trained AI model** (Scikit-learn Random Forest)

---

### Step 8: Run the Server

```bash
python manage.py runserver
```

Open your browser: **http://127.0.0.1:8000**

---

## 🔑 Login Credentials

| Role  | Username | Password  | Redirects To      |
|-------|----------|-----------|-------------------|
| Admin | admin    | admin123  | Admin Dashboard   |
| User  | demo     | demo1234  | User Dashboard    |

---

## 📁 Project Structure

```
smart_parking_system/
├── frontend/
│   ├── templates/          ← All HTML pages
│   │   ├── landing.html    ← Landing page
│   │   ├── login.html
│   │   ├── register.html
│   │   ├── admin_login.html
│   │   ├── base.html       ← User sidebar layout
│   │   ├── dashboard/
│   │   ├── booking/
│   │   ├── map/
│   │   ├── history/
│   │   ├── profile/
│   │   └── adminpanel/
│   └── static/
│       ├── css/
│       │   ├── style.css   ← Main stylesheet
│       │   └── landing.css ← Landing page styles
│       ├── js/
│       └── images/
│
├── backend/
│   ├── authentication/     ← Login, Register, Logout
│   ├── dashboard/          ← User Dashboard + AI charts
│   ├── booking/            ← Slot booking system
│   ├── map/                ← Visual parking map
│   ├── history/            ← Booking history
│   ├── profile/            ← User profile editor
│   └── adminpanel/         ← Admin views + revenue
│
├── database/
│   └── db.sqlite3          ← SQLite database
│
├── ai/
│   ├── model.py            ← Scikit-learn model builder
│   ├── training.py         ← Model training pipeline
│   └── prediction.py       ← Prediction functions
│
├── sps/                    ← Django project config
│   ├── settings.py
│   └── urls.py
│
├── manage.py
├── requirements.txt
├── setup_and_run.bat       ← Windows one-click setup
└── setup_and_run.sh        ← Mac/Linux one-click setup
```

---

## 🌐 Pages & Features

### User Side
| Page | URL | Description |
|------|-----|-------------|
| Landing | `/` | Public homepage with features |
| Login | `/auth/login/` | User login |
| Admin Login | `/auth/admin-login/` | Admin login |
| Register | `/auth/register/` | New user signup |
| Dashboard | `/dashboard/` | Slots + AI predictions + charts |
| Book Slot | `/booking/` | Reserve a parking slot |
| My Bookings | `/booking/my/` | View & cancel bookings |
| Map | `/map/` | Visual parking floor map |
| History | `/history/` | Full booking history |
| Profile | `/profile/` | Edit profile info |

### Admin Side
| Page | URL | Description |
|------|-----|-------------|
| Admin Dashboard | `/adminpanel/` | Stats + 4 revenue charts |
| Manage Slots | `/adminpanel/slots/` | Change slot status manually |
| All Users | `/adminpanel/users/` | View all registered users |
| All Bookings | `/adminpanel/bookings/` | View all bookings + vehicles |
| Revenue | `/adminpanel/revenue/` | Revenue records & totals |

---

## 🤖 AI Module

Located in `ai/`. Uses **Scikit-learn Random Forest Regressor**.

- Trains on historical + synthetic booking data
- Predicts hourly occupancy (0–100%)
- Identifies peak hours (top 3 busiest)
- Predicts next free slot availability time
- Displays crowd level: Low / Medium / High
- Dashboard charts update predictions in real time

---

## 💡 Common Issues

**"No module named django"**
→ Make sure your virtual environment is activated: `venv\Scripts\activate`

**"Port already in use"**
→ Run on different port: `python manage.py runserver 8080`

**"OperationalError: no such table"**
→ Run `python manage.py migrate` again

**CSS not loading**
→ Confirm `DEBUG = True` in `sps/settings.py`

---

## 💰 Pricing

Parking rate: **₹50 per hour** (configurable in `backend/booking/models.py`)

---

*Built with ❤️ using Django + Scikit-learn + Chart.js*
