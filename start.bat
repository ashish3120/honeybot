@echo off
set HONEYPOT_API_KEY=default_secret_key
uvicorn main:app --reload --host 0.0.0.0 --port 8000
