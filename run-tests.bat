@echo off
REM run-tests.bat

cd /d "%~dp0"

wt -w 0 new-tab -d .\backend ^
cmd /k ".venv\Scripts\python -m pytest -q -c pytest.ini"

wt -w 0 new-tab -d .\frontend ^
cmd /k "npm test -- --silent"
