# Galaxy Tools

**The #1 Twitch & Kick Automation Platform**

---

## Overview
Galaxy Tools is a premium SaaS platform for automating Twitch and Kick engagement (followers, views, chats, polls, clips, reactions, and more). Built with a world-class UI/UX, robust FastAPI backend, and direct integration with advanced automation libraries.

---

## Project Structure

```
galaxy-tools/
│
├── backend/         # FastAPI app, DB, API, services
├── frontend/        # React, TailwindCSS, Framer Motion
├── libs/            # Automation libraries (kick.py, twitch.py)
├── docs/            # Documentation (optional)
└── README.md        # This file
```

---

## Setup Instructions

### Backend
1. `cd backend`
2. Create a virtual environment: `python -m venv venv && source venv/bin/activate` (Linux/macOS) or `venv\Scripts\activate` (Windows)
3. Install dependencies: `pip install -r requirements.txt`
4. Configure `.env` (see `.env.example`)
5. Run migrations: `alembic upgrade head`
6. Start server: `uvicorn app.main:app --reload`

### Frontend
1. `cd frontend`
2. Install dependencies: `npm install`
3. Start dev server: `npm run dev`

---

## Features
- Secure JWT authentication (access/refresh)
- Email verification & password reset (SMTP configurable)
- User wallet & dashboard
- Admin panel (user management, logs, wallet controls)
- Real-time status updates (WebSocket/polling)
- Direct integration with Kick & Twitch automation libraries
- Premium, animated UI/UX (dark cosmic theme)

---

## Architecture
- **Backend:** FastAPI, PostgreSQL, Alembic, JWT, Pydantic, direct lib integration
- **Frontend:** React, TailwindCSS, Framer Motion, REST API, WebSocket

---

## License
Proprietary. All rights reserved. 