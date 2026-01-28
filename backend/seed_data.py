# backend/seed_data.py
from database.database import SessionLocal, engine
from database import models
from sqlalchemy.orm import Session
import random

# Create tables if they don't exist
models.Base.metadata.create_all(bind=engine)

db = SessionLocal()

print("🌱 Seeding Leaderboard Data...")

# 1. Create Dummy Users (if not exist)
dummy_users = ["Alice_Wonder", "Bob_Builder", "Code_Master", "Python_Pro", "Java_Junkie"]
db_users = []

for name in dummy_users:
    user = db.query(models.User).filter(models.User.username == name).first()
    if not user:
        user = models.User(
            username=name, 
            email=f"{name.lower()}@example.com", 
            password="hashedpassword"
        )
        db.add(user)
        db.commit()
        db.refresh(user)
        print(f"✅ Created User: {name}")
    else:
        print(f"ℹ️ User {name} already exists")
    db_users.append(user)

# 2. Add XP and Streak to these users
for user in db_users:
    progress = db.query(models.UserProgress).filter(models.UserProgress.user_id == user.id).first()
    if not progress:
        xp = random.randint(100, 5000)
        progress = models.UserProgress(user_id=user.id, total_xp=xp)
        db.add(progress)
        print(f"💰 Added {xp} XP to {user.username}")
    
    streak = db.query(models.Streak).filter(models.Streak.user_id == user.id).first()
    if not streak:
        days = random.randint(1, 30)
        streak = models.Streak(user_id=user.id, current_streak=days)
        db.add(streak)
        print(f"🔥 Added {days} Day Streak to {user.username}")

db.commit()
print("🎉 Seeding Complete! Leaderboard should now have data.")
db.close()