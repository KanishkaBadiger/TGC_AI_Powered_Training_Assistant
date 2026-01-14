# 🚀 AI-Powered Training Assistant

A comprehensive learning platform that combines AI, personalized learning paths, job recommendations, and competitive leaderboards to accelerate skill development.

## ✨ Features

### 1. **📋 Mock Quiz Generator**
- AI-generated quizzes covering:
  - **Aptitude**: Quantitative, Logical Reasoning, English
  - **Technical**: Python, Java, C++, JavaScript, and more
  - **Core Subjects**: OS, Database, Networks, etc.
- Multiple difficulty levels (Easy, Medium, Hard)
- Instant feedback and detailed explanations
- Performance tracking and analytics

### 2. **📄 Resume Analyzer & Skill Gap Analysis**
- Automatic resume parsing and skill extraction
- Identify missing skills for target roles
- Personalized learning recommendations
- Skill development roadmaps with timeline

### 3. **💼 Job/Internship Openings**
- Real-time job postings from multiple sources
- AI-powered job matching based on skills
- Glassdoor and PrepInsta integration
- Save and track job applications
- Personalized recommendations

### 4. **🛣️ Learning Roadmap & Calendar**
- AI-generated personalized learning paths
- Milestone tracking and progress visualization
- Structured curriculum with modules
- Timeline-based goal setting
- Resource recommendations

### 5. **🎓 Core Subjects & Aptitude Preparation**
- Comprehensive study materials
- Video tutorials and documentation links
- Practice problems with solutions
- Topic-wise performance tracking
- Difficulty level progression

### 6. **🔥 Streak & Leaderboard System**
- Daily activity streaks
- Global and category-wise leaderboards
- Weekly and monthly rankings
- Achievement badges
- Competitive scoring system

## 🛠️ Tech Stack

### Frontend
- **Streamlit** - Beautiful, responsive UI
- Pandas & Matplotlib - Data visualization
- Custom CSS for modern design

### Backend
- **FastAPI** - High-performance REST API
- Python 3.8+

### Database
- **SQLite** - Structured data storage
- **ChromaDB** - Vector database for semantic search

### AI & LLM
- **Groq API** - Fast LLM inference
- **Ollama** - Local LLM support (optional)

### Additional Libraries
- `python-jose` - JWT authentication
- `passlib` - Password hashing
- `requests` - HTTP client
- `beautifulsoup4` - Web scraping

## 📦 Installation

### Prerequisites
- Python 3.8 or higher
- pip package manager
- Git

### Backend Setup

1. **Clone the repository**
```bash
git clone <repository-url>
cd TGC_AI_Powered_Training_Assistant
```

2. **Create virtual environment**
```bash
python -m venv venv
# On Windows
venv\Scripts\activate
# On Linux/Mac
source venv/bin/activate
```

3. **Install dependencies**
```bash
pip install -r backend/requirements.txt
```

4. **Setup database**
```bash
sqlite3 database/sqlite/training_assistant.db < database/schema.sql
```

5. **Configure environment variables**
```bash
cp .env.example .env
# Edit .env and add your Groq API key
```

6. **Run backend**
```bash
uvicorn backend.main:app --reload --port 8000
```

### Frontend Setup

1. **Install Streamlit**
```bash
pip install streamlit
```

2. **Run frontend**
```bash
cd frontend
streamlit run main.py
```

## 🚀 Quick Start

### 1. **Start Backend Server**
```bash
cd backend
uvicorn main:app --reload
# Server runs on http://localhost:8000
```

### 2. **Start Frontend Application**
```bash
cd frontend
streamlit run main.py
# UI opens on http://localhost:8501
```

### 3. **Register & Login**
- Create a new account on the registration page
- Login with your credentials

### 4. **Start Learning**
- Upload your resume
- Analyze skill gaps for your target role
- Take AI-generated quizzes
- View job recommendations
- Create personalized learning roadmap

## 📚 API Endpoints

### Authentication
- `POST /api/auth/register` - Register new user
- `POST /api/auth/login` - Login user
- `GET /api/auth/profile` - Get user profile

### Quiz
- `POST /api/quiz/generate` - Generate new quiz
- `POST /api/quiz/submit-answer` - Submit quiz answer
- `POST /api/quiz/submit-session` - Complete quiz session
- `GET /api/quiz/history` - Get quiz history

### Resume
- `POST /api/resume/upload` - Upload resume
- `GET /api/resume/analysis/{id}` - Get resume analysis
- `POST /api/resume/skill-gap` - Analyze skill gaps
- `GET /api/resume/skill-development-plan` - Get development plan

### Jobs
- `GET /api/jobs/fetch` - Fetch latest jobs
- `GET /api/jobs/search` - Search jobs with filters
- `GET /api/jobs/recommended` - Get recommended jobs
- `POST /api/jobs/save` - Save job for later
- `GET /api/jobs/saved` - Get saved jobs

### Roadmap
- `POST /api/roadmap/generate` - Generate learning roadmap
- `GET /api/roadmap/{id}` - Get roadmap details
- `PUT /api/roadmap/{id}/milestone/{mid}` - Update milestone
- `GET /api/roadmap/user/roadmaps` - Get all user roadmaps

### Progress & Leaderboard
- `GET /api/progress/` - Get user progress
- `GET /api/progress/statistics` - Get detailed stats
- `GET /api/progress/streak` - Get streak info
- `GET /api/leaderboard/global` - Get global leaderboard
- `GET /api/leaderboard/user-rank` - Get user rank
- `GET /api/leaderboard/category-leaders/{category}` - Get category leaders

## 🎨 UI Features

### Beautiful Design
- Modern gradient backgrounds
- Smooth animations and transitions
- Responsive card-based layout
- Dark theme optimized for learning
- Professional typography

### Navigation
- Intuitive sidebar menu
- Quick action buttons
- Breadcrumb navigation
- Search and filter options
- Persistent session management

### Dashboard Components
- Real-time progress metrics
- Interactive charts and graphs
- Achievement badges
- Performance indicators
- Streak visualization

## 🔐 Security

- JWT-based authentication
- Password hashing with bcrypt
- Secure session management
- CORS protection
- Input validation and sanitization

## 📊 Database Schema

### Main Tables
- `users` - User accounts and profile
- `user_profiles` - Extended user information
- `quiz_questions` - Question database
- `quiz_sessions` - Quiz attempts and scores
- `quiz_attempts` - Individual question responses
- `user_progress` - Cumulative progress tracking
- `streaks` - Daily activity tracking
- `leaderboard` - User rankings
- `resumes` - Resume data and analysis
- `skill_gaps` - Skill gap analysis results
- `job_postings` - Job/internship listings
- `learning_roadmap` - Learning paths
- `roadmap_milestones` - Milestone tracking

## 🤖 LLM Integration

### Groq API Usage
- Quiz generation with varied difficulty levels
- Resume analysis and skill extraction
- Skill gap identification
- Personalized roadmap creation
- Content explanation generation

### Example: Generating Quiz
```python
from backend.services.llm_service import LLMService

questions = LLMService.generate_quiz_questions(
    category="Aptitude",
    subcategory="Quantitative",
    difficulty="medium",
    num_questions=10,
    question_type="mcq"
)
```

## 🎓 Learning Paths

### Predefined Paths
1. **Full Stack Developer** - 6 months
2. **Data Science Engineer** - 5 months
3. **DevOps Engineer** - 4 months
4. **Frontend Developer** - 3 months
5. **Backend Developer** - 5 months

## 📈 Analytics & Insights

- Performance by topic
- Accuracy trends
- Time spent per topic
- Weak areas identification
- Strengths and weaknesses analysis
- Competitive ranking

## 🐛 Troubleshooting

### Port Already in Use
```bash
# Find process using port 8000
lsof -i :8000
# Kill process
kill -9 <PID>
```

### Database Connection Error
```bash
# Recreate database
rm database/sqlite/training_assistant.db
sqlite3 database/sqlite/training_assistant.db < database/schema.sql
```

### Groq API Issues
- Verify API key in `.env`
- Check API rate limits
- Ensure internet connection

## 🤝 Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Open Pull Request

## 📝 License

This project is licensed under the MIT License - see LICENSE file for details.

## 🙏 Acknowledgments

- Groq API for fast LLM inference
- Streamlit for beautiful UI framework
- FastAPI for robust backend framework
- ChromaDB for vector database capabilities

## 📞 Support

For issues, questions, or suggestions:
- 📧 Email: support@trainingassistant.com
- 🐛 Issues: GitHub Issues
- 💬 Discussions: GitHub Discussions

## 🌟 Future Enhancements

- [ ] Mobile app (React Native)
- [ ] Real-time collaboration features
- [ ] Video tutorials integration
- [ ] AI-powered code review
- [ ] Live mock interviews
- [ ] Certifications and badges
- [ ] Advanced analytics dashboard
- [ ] API rate limiting and caching
- [ ] Multi-language support
- [ ] Dark/Light theme toggle

---

**Made with ❤️ by AI Training Team**

⭐ If you find this project helpful, please star the repository!
