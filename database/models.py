# database/models.py
from sqlalchemy import Column, Integer, String, Boolean, Date, ForeignKey, Text, JSON, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from database.database import Base

# --- USER & PROFILE ---
class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    username = Column(String, unique=True, index=True, nullable=False)
    password = Column(String, nullable=False)
    full_name = Column(String, nullable=True)
    avatar_url = Column(String, nullable=True)
    bio = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    profile = relationship("UserProfile", back_populates="user", uselist=False)
    progress = relationship("UserProgress", back_populates="user", uselist=False)
    streak = relationship("Streak", back_populates="user", uselist=False)
    leaderboard = relationship("Leaderboard", back_populates="user", uselist=False)
    roadmaps = relationship("Roadmap", back_populates="user")
    resumes = relationship("ResumeAnalysis", back_populates="user")

class UserProfile(Base):
    __tablename__ = "user_profiles"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True)
    education = Column(Text, nullable=True)
    experience_years = Column(Integer, default=0)
    current_role = Column(String, nullable=True)
    target_role = Column(String, nullable=True)
    skills = Column(Text, nullable=True)
    user = relationship("User", back_populates="profile")

# --- RESUME ANALYSIS (Restored) ---
class ResumeAnalysis(Base):
    __tablename__ = "resume_analysis"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    resume_text = Column(Text)
    analysis_result = Column(JSON) # Stores the AI analysis
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    user = relationship("User", back_populates="resumes")

# --- GAME FEATURES ---
class UserProgress(Base):
    __tablename__ = "user_progress"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True)
    total_xp = Column(Integer, default=0)
    user = relationship("User", back_populates="progress")

class Streak(Base):
    __tablename__ = "streaks"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True)
    current_streak = Column(Integer, default=0)
    last_activity_date = Column(Date, nullable=True)
    user = relationship("User", back_populates="streak")

class Leaderboard(Base):
    __tablename__ = "leaderboard"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True)
    rank = Column(Integer, default=999999)
    user = relationship("User", back_populates="leaderboard")

# --- ROADMAP ---
class Roadmap(Base):
    __tablename__ = "roadmaps"
    id = Column(Integer, primary_key=True, index=True)
    # Using Integer ForeignKey to link to users table properly
    user_id = Column(Integer, ForeignKey("users.id"), index=True)
    role = Column(String)
    skill_level = Column(String)
    start_date = Column(Date)
    end_date = Column(Date)
    is_paused = Column(Boolean, default=False)
    
    tasks = relationship("RoadmapTask", back_populates="roadmap", cascade="all, delete-orphan")
    user = relationship("User", back_populates="roadmaps")

class RoadmapTask(Base):
    __tablename__ = "roadmap_tasks"
    id = Column(Integer, primary_key=True, index=True)
    roadmap_id = Column(Integer, ForeignKey("roadmaps.id"))
    day_number = Column(Integer)
    module_name = Column(String)
    topic = Column(String)
    description = Column(Text)
    resources = Column(JSON)
    estimated_minutes = Column(Integer)
    date_assigned = Column(Date)
    status = Column(String, default="PENDING")
    
    roadmap = relationship("Roadmap", back_populates="tasks")