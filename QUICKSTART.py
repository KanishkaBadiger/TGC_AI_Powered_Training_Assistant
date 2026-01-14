#!/usr/bin/env python3
"""
Quick Start Guide for AI Training Assistant
"""

def print_banner():
    print("""
    ╔════════════════════════════════════════════════════════╗
    ║   🚀 AI-Powered Training Assistant                     ║
    ║   Complete Learning & Career Development Platform      ║
    ╚════════════════════════════════════════════════════════╝
    """)

def print_setup_instructions():
    instructions = """
    ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    📋 SETUP INSTRUCTIONS
    ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

    ✅ STEP 1: Install Python Dependencies
    ────────────────────────────────────────
    
    Windows:
    $ python -m venv venv
    $ venv\\Scripts\\activate
    
    Linux/Mac:
    $ python3 -m venv venv
    $ source venv/bin/activate
    
    $ pip install -r backend/requirements.txt
    $ pip install -r frontend/requirements.txt

    ✅ STEP 2: Setup Environment Variables
    ────────────────────────────────────────
    
    1. Copy .env.example to .env (if exists)
    2. Add your GROQ_API_KEY:
       - Go to https://console.groq.com
       - Get your API key
       - Add to .env file:
         GROQ_API_KEY=your_actual_api_key_here

    ✅ STEP 3: Initialize Database
    ────────────────────────────────────────
    
    $ python init_db.py

    ✅ STEP 4: Start Backend Server
    ────────────────────────────────────────
    
    $ cd backend
    $ uvicorn main:app --reload
    
    Backend runs at: http://localhost:8000
    API Docs available at: http://localhost:8000/docs

    ✅ STEP 5: Start Frontend (New Terminal)
    ────────────────────────────────────────
    
    $ cd frontend
    $ streamlit run main.py
    
    Frontend opens at: http://localhost:8501

    ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    🎯 FEATURES IMPLEMENTED
    ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

    ✨ 1. Mock Quiz Generator
       • AI-powered question generation using Groq
       • Categories: Aptitude, Technical, Core Subjects
       • Difficulty levels: Easy, Medium, Hard
       • Instant feedback with explanations
       • Progress tracking and analytics

    ✨ 2. Resume Analyzer & Skill Gap Analysis
       • PDF/TXT resume upload
       • Automatic skill extraction
       • Skill gap identification for target roles
       • Personalized learning recommendations
       • Development roadmaps with timelines

    ✨ 3. Job/Internship Openings
       • Integration with Glassdoor and PrepInsta
       • Real-time job postings
       • AI-powered skill matching
       • Save and track applications
       • Job recommendations based on skills

    ✨ 4. Learning Roadmap & Calendar
       • AI-generated personalized paths
       • Milestone tracking
       • Module-based curriculum
       • Resource recommendations
       • Progress visualization

    ✨ 5. Core Subjects & Aptitude Prep
       • Comprehensive study materials
       • Topic-wise practice problems
       • Difficulty progression
       • Performance analytics

    ✨ 6. Streak & Leaderboard System
       • Daily activity tracking
       • Global rankings
       • Category-wise leaderboards
       • Achievement badges
       • Competitive scoring

    ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    📚 API ENDPOINTS
    ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

    Authentication
    POST   /api/auth/register
    POST   /api/auth/login
    GET    /api/auth/profile

    Quiz
    POST   /api/quiz/generate
    POST   /api/quiz/submit-answer
    POST   /api/quiz/submit-session
    GET    /api/quiz/history

    Resume
    POST   /api/resume/upload
    GET    /api/resume/analysis/{id}
    POST   /api/resume/skill-gap
    GET    /api/resume/skill-development-plan

    Jobs
    GET    /api/jobs/fetch
    GET    /api/jobs/search
    GET    /api/jobs/recommended
    POST   /api/jobs/save
    GET    /api/jobs/saved

    Roadmap
    POST   /api/roadmap/generate
    GET    /api/roadmap/{id}
    PUT    /api/roadmap/{id}/milestone/{mid}
    GET    /api/roadmap/user/roadmaps

    Progress & Leaderboard
    GET    /api/progress/
    GET    /api/progress/statistics
    GET    /api/progress/streak
    GET    /api/leaderboard/global
    GET    /api/leaderboard/user-rank
    GET    /api/leaderboard/category-leaders/{category}

    ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    🎨 BEAUTIFUL UI FEATURES
    ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

    ✨ Modern Design
    • Gradient backgrounds
    • Dark theme optimized for learning
    • Smooth animations and transitions
    • Responsive card-based layout
    • Professional typography

    ✨ Navigation
    • Intuitive sidebar menu
    • Quick action buttons
    • Breadcrumb navigation
    • Search and filter options

    ✨ Dashboard Components
    • Real-time progress metrics
    • Interactive charts and graphs
    • Achievement badges
    • Performance indicators
    • Streak visualization

    ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    🔧 TECH STACK
    ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

    Frontend: Streamlit + Pandas + Matplotlib
    Backend: FastAPI + Python 3.8+
    Database: SQLite + ChromaDB (Vector DB)
    AI/LLM: Groq API + Ollama (optional)
    Auth: JWT + bcrypt
    API: REST with CORS support

    ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    🚀 DEPLOYMENT OPTIONS
    ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

    Option 1: Docker
    ────────────────
    $ docker-compose up

    Option 2: Manual
    ────────────────
    Terminal 1: cd backend && uvicorn main:app --reload
    Terminal 2: cd frontend && streamlit run main.py

    Option 3: Cloud Deployment
    ────────────────────────────
    • Backend: Heroku, Railway, Render
    • Frontend: Streamlit Cloud, Vercel
    • Database: AWS RDS, PostgreSQL Cloud

    ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    📂 PROJECT STRUCTURE
    ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

    TGC_AI_Powered_Training_Assistant/
    ├── backend/
    │   ├── main.py                 # FastAPI app
    │   ├── requirements.txt         # Python dependencies
    │   ├── routes/                 # API routes
    │   │   ├── auth.py
    │   │   ├── quiz.py
    │   │   ├── resume.py
    │   │   ├── jobs.py
    │   │   ├── roadmap.py
    │   │   ├── progress.py
    │   │   └── aptitude.py
    │   ├── models/                 # Pydantic models
    │   │   ├── user.py
    │   │   └── quiz.py
    │   ├── services/               # Business logic
    │   │   ├── llm_service.py
    │   │   ├── vector_service.py
    │   │   ├── job_fetcher.py
    │   │   └── resume_analyzer.py
    │   ├── db/                     # Database utilities
    │   │   ├── sqlite.py
    │   │   └── chroma.py
    │   └── utils/
    │       └── jwt_handler.py
    ├── frontend/
    │   ├── main.py                 # Streamlit app
    │   ├── requirements.txt
    │   ├── components/             # UI components
    │   ├── pages/                  # Page modules
    │   └── utils/                  # Utility functions
    ├── database/
    │   ├── schema.sql              # Database schema
    │   ├── sqlite/                 # SQLite database
    │   └── chroma/                 # Vector database
    ├── .env                        # Environment variables
    ├── docker-compose.yml          # Docker configuration
    ├── Dockerfile                  # Docker image
    ├── init_db.py                  # Database initialization
    ├── config.py                   # Configuration
    ├── README.md                   # Documentation
    └── startup.bat/.sh             # Startup scripts

    ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    🔐 SECURITY FEATURES
    ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

    ✅ JWT Authentication
    ✅ Password Hashing (bcrypt)
    ✅ Secure Session Management
    ✅ CORS Protection
    ✅ Input Validation & Sanitization
    ✅ Rate Limiting Ready
    ✅ SQL Injection Prevention

    ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    🆘 TROUBLESHOOTING
    ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

    Port Already in Use
    $ lsof -i :8000
    $ kill -9 <PID>

    Database Error
    $ rm database/sqlite/training_assistant.db
    $ python init_db.py

    API Key Issues
    1. Check .env file
    2. Verify Groq API key
    3. Check internet connection

    ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    📞 SUPPORT & RESOURCES
    ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

    📖 Documentation: See README.md
    🐛 Issues: GitHub Issues
    💬 Discussions: GitHub Discussions
    📧 Email: support@trainingassistant.com
    🌐 Website: https://trainingassistant.com

    ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    🎓 NEXT STEPS
    ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

    1. ✅ Setup dependencies
    2. ✅ Configure environment
    3. ✅ Initialize database
    4. ✅ Start backend server
    5. ✅ Start frontend application
    6. 📝 Create user account
    7. 📄 Upload resume
    8. 📋 Take first quiz
    9. 🎯 Analyze skill gaps
    10. 🛣️ Generate learning roadmap

    ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

    Made with ❤️ by AI Training Team
    Version 1.0.0

    """
    print(instructions)

if __name__ == "__main__":
    print_banner()
    print_setup_instructions()
