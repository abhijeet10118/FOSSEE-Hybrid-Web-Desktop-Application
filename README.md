# Chemical Equipment Parameter Visualizer

Hybrid Web + Desktop app for chemical equipment data. Upload CSV, view summary stats, charts, data table, last 5 uploads, and PDF reports. Django REST backend; React (web) and PyQt5 (desktop) frontends. All API access uses Basic Auth.

## Tech Stack

| Layer | Technology |
|-------|------------|
| Backend | Python, Django, Django REST Framework, Pandas, SQLite |
| Web | React, Chart.js, Vite |
| Desktop | PyQt5, Matplotlib |
| Data | CSV upload, Pandas analytics, last 5 datasets in SQLite |

## Project Structure

```
fosse/
├── backend/
│   ├── config/
│   ├── equipment_api/
│   ├── manage.py
│   ├── create_superuser.py
│   └── requirements.txt
├── web/
│   ├── src/
│   │   ├── components/
│   │   ├── api.js
│   │   └── App.jsx
│   ├── package.json
│   └── vite.config.js
├── desktop/
│   ├── ui/
│   ├── api_client.py
│   ├── main.py
│   └── requirements.txt
├── sample_equipment_data.csv
├── start_backend.bat
├── open_web_app.bat
├── open_desktop_app.bat
├── .gitignore
└── README.md
```

## One-Click Launch (Windows)

1. Double-click **start_backend.bat**  
   - Creates/uses backend venv, installs deps if needed, runs Django at http://127.0.0.1:8000  
   - Leave this window open.

2. Double-click **open_web_app.bat**  
   - Starts Vite dev server and opens http://localhost:5173 in the browser.

3. Double-click **open_desktop_app.bat**  
   - Runs the PyQt5 desktop app.

Default login (after running `python create_superuser.py` once in `backend`): **admin** / **admin123**.

## Manual Setup

### Backend

```bash
cd backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python create_superuser.py
python manage.py runserver
```

API: http://127.0.0.1:8000/api/

### Web

```bash
cd web
npm install
npm run dev
```

Open http://localhost:5173 and sign in.

### Desktop

Backend must be running. Then:

```bash
cd desktop
pip install -r requirements.txt
python main.py
```

Sign in with the same user as the web app.

## Sample Data

**sample_equipment_data.csv** in the project root. Expected columns:

- Equipment Name  
- Type  
- Flowrate  
- Pressure  
- Temperature  

Column name variants (spaces, casing) are accepted.

## Features

- CSV upload (web and desktop)
- Summary API: total count, averages, equipment type distribution
- Charts: Chart.js (web), Matplotlib (desktop)
- Last 5 uploads stored; select from history
- PDF report download per dataset
- Basic Auth on all API endpoints

## API Endpoints (Basic Auth)

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/upload/` | Upload CSV (`file`) |
| GET | `/api/history/` | Last 5 datasets |
| GET | `/api/datasets/<id>/` | Full dataset |
| GET | `/api/datasets/<id>/summary/` | Summary only |
| GET | `/api/datasets/<id>/pdf/` | PDF report |


