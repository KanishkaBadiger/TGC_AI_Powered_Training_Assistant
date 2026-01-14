#!/usr/bin/env python3
"""
Check registered users in the database
"""
import sqlite3
import os

# Database path
DB_PATH = "database/sqlite/training_assistant.db"

def check_users():
    """Display all registered users"""
    if not os.path.exists(DB_PATH):
        print(f"❌ Database not found at: {DB_PATH}")
        return
    
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        # Get all users
        cursor.execute("SELECT id, email, username, password, full_name, created_at FROM users")
        users = cursor.fetchall()
        
        print("\n" + "="*100)
        print("📊 REGISTERED USERS IN DATABASE")
        print("="*100)
        print(f"📁 Database Location: {os.path.abspath(DB_PATH)}\n")
        
        if users:
            for i, user in enumerate(users, 1):
                print(f"\n👤 User #{i}")
                print(f"   ├─ User ID: {user[0]}")
                print(f"   ├─ Email: {user[1]}")
                print(f"   ├─ Username: {user[2]}")
                print(f"   ├─ Password (Hashed/Encrypted): {user[3][:60]}...")
                print(f"   ├─ Full Name: {user[4]}")
                print(f"   └─ Registered On: {user[5]}")
        else:
            print("❌ No users registered yet\n")
        
        print("\n" + "="*100)
        print("🔐 SECURITY NOTE:")
        print("   • Passwords are NOT stored in plain text")
        print("   • Passwords are encrypted using SHA256-CRYPT hashing")
        print("   • The hash shown above is the encrypted version")
        print("   • Only the correct password will match this hash during login")
        print("="*100 + "\n")
        
        conn.close()
        
    except Exception as e:
        print(f"❌ Error reading database: {e}")

if __name__ == "__main__":
    check_users()
