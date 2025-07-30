from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import os
from app.routers_auth import router as auth_router
from app.routers_user import router as user_router
from app.routers_admin import router as admin_router
from app.routers_automation import router as automation_router

load_dotenv()

app = FastAPI(title="Galaxy Tools API")

origins = [
    os.getenv("FRONTEND_URL", "http://localhost:5173"),
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routers will be included here
# from .routers import auth, user, automation, admin
app.include_router(auth_router)
app.include_router(user_router)
app.include_router(automation_router)
app.include_router(admin_router) 