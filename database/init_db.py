# database/init_db.py
import os
from database.database import engine, Base

# CRITICAL: Import ALL models so SQLAlchemy knows they exist!
# If you don't import them here, the tables won't be created.
from database.models import User, ResumeAnalysis, Roadmap, RoadmapTask

def init_database():
    print("🔄 Connecting to database...")
    
    # This magic line creates all tables defined in models.py
    # It safely ignores tables that already exist.
    Base.metadata.create_all(bind=engine)
    
    print("✅ Database tables created successfully!")

if __name__ == "__main__":
    init_database()