@echo off
cd /d "%~dp0backend"
if not exist "venv\Scripts\activate.bat" (
    echo Creating venv...
    python -m venv venv
    call venv\Scripts\activate.bat
    pip install -r requirements.txt -q
) else (
    call venv\Scripts\activate.bat
)
echo Starting Django backend at http://127.0.0.1:8000
python manage.py runserver
