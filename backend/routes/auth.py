from fastapi import APIRouter, HTTPException
from models.user import UserRegister, UserLogin, TokenResponse, UserResponse
from db.sqlite import get_connection
from passlib.hash import sha256_crypt
from utils.jwt_handler import create_token
from datetime import datetime

router = APIRouter()

@router.post("/register", response_model=dict)
def register(user: UserRegister):
    """Register a new user"""
    conn = get_connection()
    cursor = conn.cursor()

    # Check if user already exists
    cursor.execute("SELECT id FROM users WHERE email=?", (user.email,))
    if cursor.fetchone():
        raise HTTPException(400, "User already registered with this email")
    
    cursor.execute("SELECT id FROM users WHERE username=?", (user.username,))
    if cursor.fetchone():
        raise HTTPException(400, "Username already taken")

    hashed = sha256_crypt.hash(user.password)

    try:
        cursor.execute(
            "INSERT INTO users (email, username, password, full_name, created_at) VALUES (?,?,?,?,?)",
            (user.email, user.username, hashed, user.full_name, datetime.now())
        )
        
        # Create user profile
        cursor.execute(
            "INSERT INTO user_profiles (user_id) VALUES (?)",
            (cursor.lastrowid,)
        )
        
        # Initialize progress tracking
        cursor.execute(
            "INSERT INTO user_progress (user_id) VALUES (?)",
            (cursor.lastrowid,)
        )
        
        # Initialize streak
        cursor.execute(
            "INSERT INTO streaks (user_id) VALUES (?)",
            (cursor.lastrowid,)
        )
        
        # Initialize leaderboard entry
        cursor.execute(
            "INSERT INTO leaderboard (user_id, rank) VALUES (?, ?)",
            (cursor.lastrowid, 999999)
        )
        
        conn.commit()
        return {"message": "User registered successfully", "email": user.email}
    except Exception as e:
        raise HTTPException(400, str(e))
    finally:
        conn.close()

@router.post("/login", response_model=TokenResponse)
def login(user: UserLogin):
    """Login user and return JWT token"""
    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("SELECT id, email, username, full_name, password FROM users WHERE email=?", (user.email,))
        data = cursor.fetchone()

        if not data:
            raise HTTPException(401, "Invalid credentials")
        
        user_id, email, username, full_name, hashed_pwd = data
        
        if not sha256_crypt.verify(user.password, hashed_pwd):
            raise HTTPException(401, "Invalid credentials")

        token = create_token({"user_id": user_id, "email": email})
        
        user_response = UserResponse(
            id=user_id,
            email=email,
            username=username,
            full_name=full_name,
            avatar_url=None,
            created_at=datetime.now()
        )

        return TokenResponse(
            access_token=token,
            token_type="bearer",
            user=user_response
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(400, str(e))
    finally:
        conn.close()

@router.get("/profile")
def get_profile(user_id: int):
    """Get user profile"""
    conn = get_connection()
    cursor = conn.cursor()
    
    try:
        cursor.execute(
            "SELECT id, email, username, full_name, avatar_url, bio, created_at FROM users WHERE id=?",
            (user_id,)
        )
        user_data = cursor.fetchone()
        
        if not user_data:
            raise HTTPException(404, "User not found")
        
        cursor.execute(
            "SELECT education, experience_years, current_role, target_role, skills FROM user_profiles WHERE user_id=?",
            (user_id,)
        )
        profile_data = cursor.fetchone()
        
        return {
            "id": user_data[0],
            "email": user_data[1],
            "username": user_data[2],
            "full_name": user_data[3],
            "avatar_url": user_data[4],
            "bio": user_data[5],
            "education": profile_data[0] if profile_data else None,
            "experience_years": profile_data[1] if profile_data else 0,
            "current_role": profile_data[2] if profile_data else None,
            "target_role": profile_data[3] if profile_data else None,
            "skills": profile_data[4] if profile_data else None,
        }
    finally:
        conn.close()

