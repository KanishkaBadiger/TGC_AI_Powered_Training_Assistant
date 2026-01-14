"""
Database initialization script
"""
import sqlite3
import os
from pathlib import Path

DATABASE_PATH = "./database/sqlite/training_assistant.db"
SCHEMA_PATH = "./database/schema.sql"

def init_database():
    """Initialize the database with schema"""
    try:
        # Create directory if it doesn't exist
        os.makedirs(os.path.dirname(DATABASE_PATH), exist_ok=True)
        
        # Connect to database
        conn = sqlite3.connect(DATABASE_PATH)
        cursor = conn.cursor()
        
        # Read and execute schema
        with open(SCHEMA_PATH, 'r') as f:
            schema = f.read()
            cursor.executescript(schema)
        
        conn.commit()
        conn.close()
        
        print(f"✅ Database initialized successfully at {DATABASE_PATH}")
        return True
    except FileNotFoundError:
        print(f"❌ Schema file not found at {SCHEMA_PATH}")
        return False
    except Exception as e:
        print(f"❌ Error initializing database: {e}")
        return False

def reset_database():
    """Reset the database (delete and recreate)"""
    try:
        if os.path.exists(DATABASE_PATH):
            os.remove(DATABASE_PATH)
            print(f"🗑️  Deleted existing database")
        
        return init_database()
    except Exception as e:
        print(f"❌ Error resetting database: {e}")
        return False

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "reset":
        reset_database()
    else:
        init_database()
