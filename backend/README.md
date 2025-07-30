# Galaxy Tools Backend

## Setup
1. Create and activate a virtual environment:
   - `python -m venv venv && source venv/bin/activate` (Linux/macOS)
   - `venv\Scripts\activate` (Windows)
2. Install dependencies:
   - `pip install -r requirements.txt`
3. Configure environment variables in `.env` (see `.env.example`).
4. Run database migrations:
   - `alembic upgrade head`
5. Start the server:
   - `uvicorn app.main:app --reload`

## Environment Variables
- `DATABASE_URL` (PostgreSQL connection string)
- `JWT_SECRET_KEY`, `JWT_REFRESH_SECRET_KEY`
- `SMTP_SERVER`, `SMTP_PORT`, `SMTP_USER`, `SMTP_PASSWORD`, `EMAIL_FROM`

## Architecture
- **FastAPI** for API
- **PostgreSQL** for DB
- **Alembic** for migrations
- **JWT** for authentication
- **Direct integration** with `libs/kick.py` and `libs/twitch.py`

## Features
- User registration, login, email verification, password reset
- Wallet management
- Automation endpoints (Kick & Twitch)
- Admin panel endpoints
- Secure, validated, and scalable 