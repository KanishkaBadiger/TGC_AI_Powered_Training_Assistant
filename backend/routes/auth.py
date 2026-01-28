# from fastapi import APIRouter, HTTPException
# from models.user import UserRegister, UserLogin, TokenResponse, UserResponse
# from db.sqlite import get_connection
# from passlib.hash import sha256_crypt
# from utils.jwt_handler import create_token
# from datetime import datetime

# router = APIRouter()

# @router.post("/register", response_model=dict)
# def register(user: UserRegister):
#     """Register a new user"""
#     conn = get_connection()
#     cursor = conn.cursor()

#     # Check if user already exists
#     cursor.execute("SELECT id FROM users WHERE email=?", (user.email,))
#     if cursor.fetchone():
#         raise HTTPException(400, "User already registered with this email")
    
#     cursor.execute("SELECT id FROM users WHERE username=?", (user.username,))
#     if cursor.fetchone():
#         raise HTTPException(400, "Username already taken")

#     hashed = sha256_crypt.hash(user.password)

#     try:
#         cursor.execute(
#             "INSERT INTO users (email, username, password, full_name, created_at) VALUES (?,?,?,?,?)",
#             (user.email, user.username, hashed, user.full_name, datetime.now())
#         )
        
#         # Create user profile
#         cursor.execute(
#             "INSERT INTO user_profiles (user_id) VALUES (?)",
#             (cursor.lastrowid,)
#         )
        
#         # Initialize progress tracking
#         cursor.execute(
#             "INSERT INTO user_progress (user_id) VALUES (?)",
#             (cursor.lastrowid,)
#         )
        
#         # Initialize streak
#         cursor.execute(
#             "INSERT INTO streaks (user_id) VALUES (?)",
#             (cursor.lastrowid,)
#         )
        
#         # Initialize leaderboard entry
#         cursor.execute(
#             "INSERT INTO leaderboard (user_id, rank) VALUES (?, ?)",
#             (cursor.lastrowid, 999999)
#         )
        
#         conn.commit()
#         return {"message": "User registered successfully", "email": user.email}
#     except Exception as e:
#         raise HTTPException(400, str(e))
#     finally:
#         conn.close()

# @router.post("/login", response_model=TokenResponse)
# def login(user: UserLogin):
#     """Login user and return JWT token"""
#     conn = get_connection()
#     cursor = conn.cursor()

#     try:
#         cursor.execute("SELECT id, email, username, full_name, password FROM users WHERE email=?", (user.email,))
#         data = cursor.fetchone()

#         if not data:
#             raise HTTPException(401, "Invalid credentials")
        
#         user_id, email, username, full_name, hashed_pwd = data
        
#         if not sha256_crypt.verify(user.password, hashed_pwd):
#             raise HTTPException(401, "Invalid credentials")

#         token = create_token({"user_id": user_id, "email": email})
        
#         user_response = UserResponse(
#             id=user_id,
#             email=email,
#             username=username,
#             full_name=full_name,
#             avatar_url=None,
#             created_at=datetime.now()
#         )

#         return TokenResponse(
#             access_token=token,
#             token_type="bearer",
#             user=user_response
#         )
#     except HTTPException:
#         raise
#     except Exception as e:
#         raise HTTPException(400, str(e))
#     finally:
#         conn.close()

# @router.get("/profile")
# def get_profile(user_id: int):
#     """Get user profile"""
#     conn = get_connection()
#     cursor = conn.cursor()
    
#     try:
#         cursor.execute(
#             "SELECT id, email, username, full_name, avatar_url, bio, created_at FROM users WHERE id=?",
#             (user_id,)
#         )
#         user_data = cursor.fetchone()
        
#         if not user_data:
#             raise HTTPException(404, "User not found")
        
#         cursor.execute(
#             "SELECT education, experience_years, current_role, target_role, skills FROM user_profiles WHERE user_id=?",
#             (user_id,)
#         )
#         profile_data = cursor.fetchone()
        
#         return {
#             "id": user_data[0],
#             "email": user_data[1],
#             "username": user_data[2],
#             "full_name": user_data[3],
#             "avatar_url": user_data[4],
#             "bio": user_data[5],
#             "education": profile_data[0] if profile_data else None,
#             "experience_years": profile_data[1] if profile_data else 0,
#             "current_role": profile_data[2] if profile_data else None,
#             "target_role": profile_data[3] if profile_data else None,
#             "skills": profile_data[4] if profile_data else None,
#         }
#     finally:
#         conn.close()


# backend/routes/auth.py
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from datetime import datetime
from passlib.hash import sha256_crypt

# New Imports
from database.database import get_db
from database import models
from models.user import UserRegister, UserLogin, TokenResponse, UserResponse
from utils.jwt_handler import create_token

router = APIRouter()

@router.post("/register", response_model=dict)
def register(user: UserRegister, db: Session = Depends(get_db)):
    """Register a new user using SQLAlchemy"""
    
    # 1. Check existing user
    if db.query(models.User).filter(models.User.email == user.email).first():
        raise HTTPException(400, "User already registered with this email")
    
    if db.query(models.User).filter(models.User.username == user.username).first():
        raise HTTPException(400, "Username already taken")

    # 2. Hash Password
    hashed_pwd = sha256_crypt.hash(user.password)

    # 3. Create User Object
    new_user = models.User(
        email=user.email,
        username=user.username,
        password=hashed_pwd,
        full_name=user.full_name,
        created_at=datetime.now()
    )
    
    try:
        db.add(new_user)
        db.commit()
        db.refresh(new_user) # Get the new ID

        # # 4. Create Linked Tables (Profile, Streak, etc.)
        # new_profile = models.UserProfile(user_id=new_user.id)
        # new_progress = models.UserProgress(user_id=new_user.id)
        # new_streak = models.Streak(user_id=new_user.id)
        # new_leaderboard = models.Leaderboard(user_id=new_user.id, rank=999999)

        # db.add_all([new_profile, new_progress, new_streak, new_leaderboard])
        # db.commit()

        return {"message": "User registered successfully", "email": user.email}

    except Exception as e:
        db.rollback() # Undo changes if error
        raise HTTPException(400, f"Registration failed: {str(e)}")


@router.post("/login", response_model=TokenResponse)
def login(user: UserLogin, db: Session = Depends(get_db)):
    """Login user using SQLAlchemy"""
    
    # 1. Find User
    db_user = db.query(models.User).filter(models.User.email == user.email).first()

    if not db_user:
        raise HTTPException(401, "Invalid credentials")

    # 2. Verify Password
    if not sha256_crypt.verify(user.password, db_user.password):
        raise HTTPException(401, "Invalid credentials")

    # 3. Generate Token
    token = create_token({"user_id": db_user.id, "email": db_user.email})

    # 4. Prepare Response
    user_resp = UserResponse(
        id=db_user.id,
        email=db_user.email,
        username=db_user.username,
        full_name=db_user.full_name,
        avatar_url=db_user.avatar_url,
        created_at=db_user.created_at
    )

    return TokenResponse(
        access_token=token,
        token_type="bearer",
        user=user_resp
    )


@router.get("/profile")
def get_profile(user_id: int, db: Session = Depends(get_db)):
    """Get profile using SQLAlchemy"""
    
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    if not db_user:
        raise HTTPException(404, "User not found")
    
    # SQLAlchemy automatically fetches the related profile via relationships
    profile = db_user.profile 

    return {
        "id": db_user.id,
        "email": db_user.email,
        "username": db_user.username,
        "full_name": db_user.full_name,
        "avatar_url": db_user.avatar_url,
        "bio": db_user.bio,
        # Handle case where profile might be empty (though we create it on register)
        "education": profile.education if profile else None,
        "experience_years": profile.experience_years if profile else 0,
        "current_role": profile.current_role if profile else None,
        "target_role": profile.target_role if profile else None,
        "skills": profile.skills if profile else None,
    }