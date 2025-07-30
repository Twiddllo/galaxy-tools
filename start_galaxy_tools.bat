@echo off
REM Start Galaxy Tools Backend and Frontend

REM Activate backend venv and start FastAPI
start cmd /k "cd backend && uvicorn app.main:app --reload"

REM Start React frontend
start cmd /k "cd frontend && npm start"

REM Optional: Wait for user to close
pause 