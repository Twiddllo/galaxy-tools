from fastapi import APIRouter, Depends, HTTPException, status, BackgroundTasks
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.database import get_db
from app.models import User, Wallet
from app.schemas import UserCreate, UserOut, Token, EmailRequest, PasswordResetRequest, PasswordResetConfirm
from app.utils import hash_password, verify_password, create_access_token, create_refresh_token, send_email
from pydantic import EmailStr
from jose import jwt, JWTError
from datetime import timedelta, datetime
import os

router = APIRouter(prefix="/auth", tags=["auth"])

FRONTEND_URL = os.getenv("FRONTEND_URL", "http://localhost:5173")
JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")
ALGORITHM = "HS256"

# Registration
@router.post("/register", response_model=UserOut)
async def register(user: UserCreate, db: AsyncSession = Depends(get_db), background_tasks: BackgroundTasks = None):
    if user.password != user.confirm_password:
        raise HTTPException(status_code=400, detail="Passwords do not match.")
    result = await db.execute(select(User).where((User.username == user.username) | (User.email == user.email)))
    if result.scalar():
        raise HTTPException(status_code=400, detail="Username or email already exists.")
    hashed = hash_password(user.password)
    db_user = User(
        username=user.username,
        first_name=user.first_name,
        last_name=user.last_name,
        email=user.email,
        phone=user.phone,
        password_hash=hashed,
        is_active=True,
        is_verified=False,
        is_admin=False,
    )
    db.add(db_user)
    await db.flush()
    db_wallet = Wallet(user_id=db_user.id, balance=0.0)
    db.add(db_wallet)
    await db.commit()
    await db.refresh(db_user)
    # Email verification
    token = create_access_token({"sub": db_user.email}, expires_delta=timedelta(hours=24))
    verify_url = f"{FRONTEND_URL}/verify-email?token={token}"
    html = f"""
    <h2>Welcome to Galaxy Tools!</h2>
    <p>Click <a href='{verify_url}'>here</a> to verify your email.</p>
    <p>If you did not sign up, ignore this email.</p>
    """
    if background_tasks:
        background_tasks.add_task(send_email, db_user.email, "Verify your Galaxy Tools account", html)
    else:
        send_email(db_user.email, "Verify your Galaxy Tools account", html)
    return db_user

# Email verification
@router.get("/verify-email")
async def verify_email(token: str, db: AsyncSession = Depends(get_db)):
    try:
        payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=[ALGORITHM])
        email = payload.get("sub")
        if not email:
            raise HTTPException(status_code=400, detail="Invalid token.")
    except JWTError:
        raise HTTPException(status_code=400, detail="Invalid or expired token.")
    result = await db.execute(select(User).where(User.email == email))
    user = result.scalar()
    if not user:
        raise HTTPException(status_code=404, detail="User not found.")
    if user.is_verified:
        return {"message": "Email already verified."}
    user.is_verified = True
    await db.commit()
    return {"message": "Email verified successfully."}

# Login
@router.post("/login", response_model=Token)
async def login(form: EmailRequest, password: str, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(User).where(User.email == form.email))
    user = result.scalar()
    if not user or not verify_password(password, user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid credentials.")
    if not user.is_verified:
        raise HTTPException(status_code=403, detail="Email not verified.")
    access_token = create_access_token({"sub": str(user.id)})
    refresh_token = create_refresh_token({"sub": str(user.id)})
    return Token(access_token=access_token, refresh_token=refresh_token)

# Password reset request
@router.post("/password-reset-request")
async def password_reset_request(req: PasswordResetRequest, db: AsyncSession = Depends(get_db), background_tasks: BackgroundTasks = None):
    result = await db.execute(select(User).where(User.email == req.email))
    user = result.scalar()
    if not user:
        return {"message": "If the email exists, a reset link will be sent."}
    token = create_access_token({"sub": user.email}, expires_delta=timedelta(hours=1))
    reset_url = f"{FRONTEND_URL}/reset-password?token={token}"
    html = f"""
    <h2>Galaxy Tools Password Reset</h2>
    <p>Click <a href='{reset_url}'>here</a> to reset your password.</p>
    <p>If you did not request this, ignore this email.</p>
    """
    if background_tasks:
        background_tasks.add_task(send_email, user.email, "Reset your Galaxy Tools password", html)
    else:
        send_email(user.email, "Reset your Galaxy Tools password", html)
    return {"message": "If the email exists, a reset link will be sent."}

# Password reset confirm
@router.post("/password-reset-confirm")
async def password_reset_confirm(data: PasswordResetConfirm, db: AsyncSession = Depends(get_db)):
    try:
        payload = jwt.decode(data.token, JWT_SECRET_KEY, algorithms=[ALGORITHM])
        email = payload.get("sub")
        if not email:
            raise HTTPException(status_code=400, detail="Invalid token.")
    except JWTError:
        raise HTTPException(status_code=400, detail="Invalid or expired token.")
    result = await db.execute(select(User).where(User.email == email))
    user = result.scalar()
    if not user:
        raise HTTPException(status_code=404, detail="User not found.")
    if data.new_password != data.confirm_password:
        raise HTTPException(status_code=400, detail="Passwords do not match.")
    user.password_hash = hash_password(data.new_password)
    await db.commit()
    return {"message": "Password reset successful."} 