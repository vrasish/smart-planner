# Local Setup Guide - Smart Planner

Everything runs on your local machine. No cloud deployment needed.

## What You Have

- **Database**: MySQL in DBeaver (localhost:3306)
- **Backend**: FastAPI on localhost:8000
- **Frontend**: HTML files served via XAMPP (localhost/smartplanner)

---

## How to Run Locally

### Step 1: Start MySQL (XAMPP)

1. Open XAMPP Control Panel
2. Start **MySQL** service
3. Make sure it's running (green)

### Step 2: Start Backend API

In Terminal:

```bash
cd /Applications/XAMPP/xamppfiles/htdocs/smartplanner
source venv/bin/activate
uvicorn api:app --reload
```

Keep this terminal open. The API will run at `http://localhost:8000`

### Step 3: Access Frontend

1. Make sure **Apache** is running in XAMPP
2. Open browser: `http://localhost/smartplanner/login.html`
3. Or: `http://localhost/smartplanner/index.html`

---

## Database Setup (One-time)

Your database should already be set up in DBeaver. If not:

1. **Open DBeaver**
2. **Connect to**: `localhost:3306`, database: `smartplanner`
3. **Run the SQL** from `setup.sql` or run:
   ```bash
   python setup_users.py
   python setup_extended_features.py
   ```

---

## Default Users

- **Admin**: `admin` / `admin123.`
- **Students**: `Vaishnavi`, `Student2`, `Student3`, `Student4` / `student`

---

## Quick Start Commands

```bash
# Terminal 1: Start backend
cd /Applications/XAMPP/xamppfiles/htdocs/smartplanner
source venv/bin/activate
uvicorn api:app --reload

# Terminal 2: (Optional) Run setup scripts if needed
cd /Applications/XAMPP/xamppfiles/htdocs/smartplanner
source venv/bin/activate
python setup_users.py
python setup_extended_features.py
```

---

## Access URLs

- **Frontend**: http://localhost/smartplanner/login.html
- **Backend API**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs

---

## That's It!

Everything runs locally. No cloud services needed. Just:
1. Start MySQL in XAMPP
2. Start backend API (`uvicorn api:app --reload`)
3. Open frontend in browser
