@echo off
REM run-servers.bat

cd /d "%~dp0"

wt -w 0 new-tab -d .\backend ^
cmd /k ".venv\Scripts\python manage.py runserver"

wt -w 0 new-tab -d .\frontend ^
cmd /k "npm run dev"
