from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.database import get_db
from app.models import User, Wallet, AdminLog
from app.schemas import UserOut, WalletOut
from jose import jwt, JWTError
from fastapi.security import OAuth2PasswordBearer
from typing import List, Optional
import os

router = APIRouter(prefix="/admin", tags=["admin"])

JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")
ALGORITHM = "HS256"
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

async def get_current_admin(token: str = Depends(oauth2_scheme), db: AsyncSession = Depends(get_db)):
    credentials_exception = HTTPException(status_code=401, detail="Could not validate credentials")
    try:
        payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("sub")
        if user_id is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    result = await db.execute(select(User).where(User.id == int(user_id)))
    user = result.scalar()
    if user is None or not user.is_admin:
        raise credentials_exception
    return user

@router.get("/users", response_model=List[UserOut])
async def list_users(
    q: Optional[str] = Query(None),
    skip: int = 0,
    limit: int = 20,
    db: AsyncSession = Depends(get_db),
    admin: User = Depends(get_current_admin),
):
    query = select(User)
    if q:
        query = query.where((User.username.ilike(f"%{q}%")) | (User.email.ilike(f"%{q}%")))
    result = await db.execute(query.offset(skip).limit(limit))
    return result.scalars().all()

@router.get("/user/{user_id}", response_model=UserOut)
async def get_user(user_id: int, db: AsyncSession = Depends(get_db), admin: User = Depends(get_current_admin)):
    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalar()
    if not user:
        raise HTTPException(status_code=404, detail="User not found.")
    return user

@router.patch("/user/{user_id}")
async def edit_user(user_id: int, is_active: Optional[bool] = None, is_admin: Optional[bool] = None, db: AsyncSession = Depends(get_db), admin: User = Depends(get_current_admin)):
    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalar()
    if not user:
        raise HTTPException(status_code=404, detail="User not found.")
    if is_active is not None:
        user.is_active = is_active
    if is_admin is not None:
        user.is_admin = is_admin
    await db.commit()
    return {"message": "User updated."}

@router.delete("/user/{user_id}")
async def delete_user(user_id: int, db: AsyncSession = Depends(get_db), admin: User = Depends(get_current_admin)):
    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalar()
    if not user:
        raise HTTPException(status_code=404, detail="User not found.")
    await db.delete(user)
    await db.commit()
    return {"message": "User deleted."}

@router.post("/wallet/{user_id}/adjust")
async def adjust_wallet(user_id: int, amount: float, db: AsyncSession = Depends(get_db), admin: User = Depends(get_current_admin)):
    result = await db.execute(select(Wallet).where(Wallet.user_id == user_id))
    wallet = result.scalar()
    if not wallet:
        raise HTTPException(status_code=404, detail="Wallet not found.")
    wallet.balance += amount
    await db.commit()
    return {"message": "Wallet balance updated.", "balance": wallet.balance}

@router.get("/logs")
async def get_logs(skip: int = 0, limit: int = 50, db: AsyncSession = Depends(get_db), admin: User = Depends(get_current_admin)):
    result = await db.execute(select(AdminLog).offset(skip).limit(limit))
    logs = result.scalars().all()
    return logs 