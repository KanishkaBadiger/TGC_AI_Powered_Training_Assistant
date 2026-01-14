from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime

class UserRegister(BaseModel):
    email: EmailStr
    username: str
    password: str
    full_name: Optional[str] = None

class UserLogin(BaseModel):
    email: str
    password: str

class UserProfile(BaseModel):
    id: Optional[int] = None
    user_id: int
    education: Optional[str] = None
    experience_years: int = 0
    current_role: Optional[str] = None
    target_role: Optional[str] = None
    skills: Optional[List[str]] = None

class UserUpdate(BaseModel):
    full_name: Optional[str] = None
    avatar_url: Optional[str] = None
    bio: Optional[str] = None
    current_role: Optional[str] = None
    target_role: Optional[str] = None
    skills: Optional[List[str]] = None

class UserResponse(BaseModel):
    id: int
    email: str
    username: str
    full_name: Optional[str]
    avatar_url: Optional[str]
    created_at: datetime

class TokenResponse(BaseModel):
    access_token: str
    token_type: str
    user: UserResponse

class ProgressResponse(BaseModel):
    email: str
    progress: str
    level: str
    total_quizzes_attempted: int
    current_streak: int
    max_streak: int
