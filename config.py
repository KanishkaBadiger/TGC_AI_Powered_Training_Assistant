"""
Configuration for AI Training Assistant
"""
import os
from dotenv import load_dotenv

load_dotenv()

# API Configuration
API_HOST = os.getenv("API_HOST", "0.0.0.0")
API_PORT = int(os.getenv("BACKEND_PORT", "8000"))
DEBUG = os.getenv("DEBUG", "True") == "True"

# Frontend Configuration
FRONTEND_PORT = int(os.getenv("FRONTEND_PORT", "8501"))
API_BASE_URL = os.getenv("API_BASE_URL", "http://localhost:8000")

# Database Configuration
DATABASE_PATH = os.getenv("DATABASE_PATH", "./database/sqlite/training_assistant.db")
CHROMA_DB_PATH = os.getenv("CHROMA_DB_PATH", "./database/chroma")

# JWT Configuration
SECRET_KEY = os.getenv("SECRET_KEY", "your-super-secret-key-change-in-production")
ALGORITHM = os.getenv("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))

# Groq Configuration
GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")

# Job API Configuration
JSEARCH_API_KEY = os.getenv("JSEARCH_API_KEY", "")

# Environment
ENVIRONMENT = os.getenv("ENVIRONMENT", "development")

# Logging
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")

# CORS Settings
CORS_ORIGINS = ["*"]
CORS_CREDENTIALS = True
CORS_METHODS = ["*"]
CORS_HEADERS = ["*"]
