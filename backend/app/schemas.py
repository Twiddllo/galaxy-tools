from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List
import datetime

class UserBase(BaseModel):
    username: str
    first_name: str
    last_name: str
    email: EmailStr
    phone: Optional[str] = None

class UserCreate(UserBase):
    password: str
    confirm_password: str

class UserOut(UserBase):
    id: int
    is_active: bool
    is_verified: bool
    is_admin: bool
    created_at: datetime.datetime
    class Config:
        orm_mode = True

class WalletOut(BaseModel):
    balance: float
    class Config:
        orm_mode = True

class AutomationRequestCreate(BaseModel):
    platform: str
    feature: str
    parameters: dict

class AutomationRequestOut(BaseModel):
    id: int
    platform: str
    feature: str
    parameters: dict
    status: str
    created_at: datetime.datetime
    updated_at: datetime.datetime
    class Config:
        orm_mode = True

class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"

class TokenData(BaseModel):
    user_id: Optional[int] = None

class EmailRequest(BaseModel):
    email: EmailStr

class PasswordResetRequest(BaseModel):
    email: EmailStr

class PasswordResetConfirm(BaseModel):
    token: str
    new_password: str
    confirm_password: str 