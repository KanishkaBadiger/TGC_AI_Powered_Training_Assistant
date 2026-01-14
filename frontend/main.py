import streamlit as st
import requests
import json
from datetime import datetime
import pandas as pd
import time
import plotly.graph_objects as go
import plotly.express as px

# Configure page
st.set_page_config(
    page_title="AI Training Assistant",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Professional Modern Color Scheme CSS with White Background
st.markdown("""
<style>
    * {
        margin: 0;
        padding: 0;
        box-sizing: border-box;
    }
    
    body, html {
        background: #ffffff;
        color: #2d3142;
        font-family: 'Segoe UI', 'Trebuchet MS', sans-serif;
    }
    
    .main {
        background: #ffffff;
        color: #2d3142;
        padding: 30px;
    }
    
    /* Sidebar Styling */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #f0f4f8 0%, #e8ecf1 100%) !important;
    }
    
    [data-testid="stSidebar"] [data-testid="stMarkdownContainer"] {
        color: #2d3142 !important;
    }
    
    [data-testid="stSidebar"] * {
        color: #2d3142 !important;
    }
    
    [data-testid="stSidebar"] h1, [data-testid="stSidebar"] h2, [data-testid="stSidebar"] h3 {
        color: #2d3142 !important;
    }
    
    [data-testid="stSidebar"] label {
        color: #2d3142 !important;
    }
    
    /* Hide sidebar on auth pages */
    .hide-sidebar [data-testid="stSidebar"] {
        display: none !important;
    }
    
    /* Header Styles - Modern Gradient */
    .header-main {
        background: linear-gradient(135deg, #23b5d3 0%, #62929e 100%);
        padding: 60px 50px;
        border-radius: 20px;
        text-align: center;
        color: #ffffff;
        margin-bottom: 40px;
        box-shadow: 0 15px 50px rgba(35, 181, 211, 0.25);
        animation: slideDown 0.6s ease-out;
        border: none;
    }
    
    .header-main h1 {
        font-size: 3.5rem;
        font-weight: 900;
        margin-bottom: 15px;
        text-shadow: 0 2px 8px rgba(0,0,0,0.2);
        color: #ffffff;
        letter-spacing: -0.5px;
    }
    
    .header-main p {
        font-size: 1.3rem;
        opacity: 0.95;
        font-weight: 500;
        color: #ffffff;
        letter-spacing: 0.5px;
    }
    
    /* Professional Card Styles */
    .card {
        background: linear-gradient(135deg, #e8f4f8 0%, #f0f8fc 100%);
        border: 2px solid #23b5d3;
        border-left: 6px solid #ef8354;
        border-radius: 12px;
        padding: 25px;
        margin: 15px 0;
        box-shadow: 0 6px 20px rgba(35, 181, 211, 0.15);
        transition: all 0.3s cubic-bezier(0.4, 0.0, 0.2, 1);
    }
    
    .card:hover {
        border-left-color: #23b5d3;
        border-color: #ef8354;
        box-shadow: 0 15px 35px rgba(239, 131, 84, 0.2);
        transform: translateY(-6px);
    }
    
    .card-title {
        font-size: 1.4rem;
        font-weight: 700;
        color: #2d3142;
        margin-bottom: 10px;
        border-bottom: 2px solid #23b5d3;
        padding-bottom: 10px;
    }
    
    /* Feature Cards - Modern Grid */
    .feature-card {
        background: linear-gradient(135deg, #ffffff 0%, #f0f9fb 100%);
        border: 2px solid #23b5d3;
        border-radius: 15px;
        padding: 30px;
        text-align: center;
        transition: all 0.3s ease;
        cursor: pointer;
        position: relative;
        overflow: hidden;
    }
    
    .feature-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 5px;
        background: linear-gradient(90deg, #ef8354, #23b5d3, #62929e);
    }
    
    .feature-card:hover {
        border-color: #23b5d3;
        box-shadow: 0 15px 40px rgba(35, 181, 211, 0.2);
        transform: translateY(-8px);
    }
    
    .feature-icon {
        font-size: 3.5rem;
        margin-bottom: 15px;
        animation: bounce 2s infinite;
    }
    
    .feature-name {
        font-size: 1.3rem;
        font-weight: 700;
        color: #2d3142;
        margin-bottom: 10px;
    }
    
    .feature-desc {
        font-size: 0.95rem;
        color: #4f5d75;
        line-height: 1.6;
    }
    
    /* Project Info Cards */
    .info-card {
        background: linear-gradient(135deg, #fef5f1 0%, #fef9f5 100%);
        border-left: 6px solid #ef8354;
        border-radius: 10px;
        padding: 20px;
        margin: 12px 0;
        transition: all 0.3s ease;
        border-top: 2px solid #23b5d3;
    }
    
    .info-card:hover {
        border-left-color: #23b5d3;
        background: linear-gradient(135deg, #fffaf8 0%, #ffffff 100%);
        box-shadow: 0 10px 25px rgba(239, 131, 84, 0.2);
        transform: translateX(8px);
    }
    
    .info-card-title {
        font-size: 1.1rem;
        font-weight: 700;
        color: #23b5d3;
        margin-bottom: 8px;
    }
    
    .info-card-desc {
        font-size: 0.95rem;
        color: #4f5d75;
        line-height: 1.6;
    }
    
    /* Button Styles - Premium */
    .stButton > button {
        background: linear-gradient(135deg, #ef8354 0%, #e07040 100%) !important;
        color: white !important;
        border: none !important;
        border-radius: 10px !important;
        padding: 12px 32px !important;
        font-weight: 700 !important;
        font-size: 1rem !important;
        transition: all 0.3s ease !important;
        text-transform: uppercase !important;
        letter-spacing: 0.5px !important;
        box-shadow: 0 8px 20px rgba(239, 131, 84, 0.3) !important;
    }
    
    .stButton > button:hover {
        box-shadow: 0 15px 35px rgba(239, 131, 84, 0.5) !important;
        transform: translateY(-3px) !important;
        background: linear-gradient(135deg, #f09060 0%, #e85c3c 100%) !important;
    }
    
    /* Input Styles */
    .stTextInput > div > div > input,
    .stPasswordInput > div > div > input,
    .stSelectbox > div > div > select,
    .stTextArea > div > div > textarea,
    .stNumberInput > div > div > input {
        background: #ffffff !important;
        border: 2px solid #e0e0e0 !important;
        color: #2d3142 !important;
        border-radius: 10px !important;
        padding: 12px 15px !important;
        font-size: 1rem !important;
        transition: all 0.3s ease !important;
    }
    
    .stTextInput > div > div > input:focus,
    .stPasswordInput > div > div > input:focus,
    .stSelectbox > div > div > select:focus,
    .stTextArea > div > div > textarea:focus,
    .stNumberInput > div > div > input:focus {
        border-color: #23b5d3 !important;
        box-shadow: 0 0 0 3px rgba(35, 181, 211, 0.1) !important;
        background: #ffffff !important;
    }
    
    /* Metrics - Modern Cards */
    .stMetric {
        background: linear-gradient(135deg, #ffffff 0%, #f5f7fa 100%) !important;
        border: 2px solid #e0e0e0 !important;
        border-top: 4px solid #23b5d3 !important;
        padding: 25px !important;
        border-radius: 12px !important;
        transition: all 0.3s ease !important;
    }
    
    .stMetric:hover {
        border-top-color: #ef8354 !important;
        transform: translateY(-5px) !important;
        box-shadow: 0 12px 30px rgba(35, 181, 211, 0.15) !important;
    }
    
    /* Messages */
    .stSuccess {
        background: #e8f5e9 !important;
        border-left: 4px solid #4caf50 !important;
        border-radius: 8px !important;
        padding: 15px !important;
        color: #2d3142 !important;
    }
    
    .stError {
        background: #ffebee !important;
        border-left: 4px solid #ef8354 !important;
        border-radius: 8px !important;
        padding: 15px !important;
        color: #2d3142 !important;
    }
    
    .stWarning {
        background: #fff3e0 !important;
        border-left: 4px solid #ff9800 !important;
        border-radius: 8px !important;
        padding: 15px !important;
        color: #2d3142 !important;
    }
    
    .stInfo {
        background: #e1f5fe !important;
        border-left: 4px solid #23b5d3 !important;
        border-radius: 8px !important;
        padding: 15px !important;
        color: #2d3142 !important;
    }
    
    /* Animations */
    @keyframes slideDown {
        from {
            opacity: 0;
            transform: translateY(-30px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    @keyframes bounce {
        0%, 100% { transform: translateY(0); }
        50% { transform: translateY(-15px); }
    }
    
    /* Divider */
    hr {
        border: none;
        height: 2px;
        background: linear-gradient(90deg, transparent, #e0e0e0, transparent);
        margin: 30px 0;
    }
    
    h2 { 
        color: #2d3142 !important; 
        border-bottom: 3px solid #23b5d3; 
        padding-bottom: 10px; 
        font-weight: 800 !important;
        font-size: 2rem !important;
    }
    
    h3 { 
        color: #23b5d3 !important; 
        font-weight: 700 !important;
        font-size: 1.5rem !important;
    }
    
    h4 { 
        color: #62929e !important; 
        font-weight: 600 !important;
    }
    
    p { 
        color: #4f5d75;
        line-height: 1.7;
    }
    
    /* Sidebar Radio Button Styling */
    [data-testid="stSidebar"] .stRadio > label {
        color: #ffffff !important;
        font-weight: 600 !important;
    }
    
    [data-testid="stSidebar"] .stRadio > div {
        gap: 15px !important;
    }
</style>
""", unsafe_allow_html=True)

# API Configuration
API_BASE_URL = "http://localhost:8000/api"

def init_session_state():
    """Initialize session state"""
    if "token" not in st.session_state:
        st.session_state.token = None
    if "user" not in st.session_state:
        st.session_state.user = None
    if "page" not in st.session_state:
        st.session_state.page = "login"

init_session_state()

def get_headers():
    """Get request headers"""
    headers = {"Content-Type": "application/json"}
    if st.session_state.token:
        headers["Authorization"] = f"Bearer {st.session_state.token}"
    return headers

# ===== LOGIN PAGE =====

def login_page():
    """Professional Login Page"""
    # Hide sidebar on login page
    st.markdown("""
    <style>
        [data-testid="stSidebar"] { display: none !important; }
    </style>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class='header-main'>
        <h1>🎓 AI Training Assistant</h1>
        <p>Master Your Skills with AI-Powered Learning</p>
    </div>
    """, unsafe_allow_html=True)
    
    col_left, col_right = st.columns([1.2, 1])
    
    with col_left:
        st.markdown("""
        <div class='card'>
            <h2 class='card-title'>Welcome Back!</h2>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("### Sign In to Your Account")
        
        email = st.text_input("📧 Email Address", placeholder="your@email.com", key="login_email")
        password = st.text_input("🔐 Password", type="password", placeholder="Enter your password", key="login_pass")
        
        col_signin_1, col_signin_2 = st.columns(2)
        
        with col_signin_1:
            if st.button("🔓 Sign In", use_container_width=True, key="btn_login"):
                if email and password:
                    try:
                        response = requests.post(
                            f"{API_BASE_URL}/auth/login",
                            json={"email": email, "password": password},
                            headers=get_headers()
                        )
                        
                        if response.status_code == 200:
                            data = response.json()
                            st.session_state.token = data.get("access_token")
                            st.session_state.user = data.get("user")
                            st.success("✅ Login successful!")
                            time.sleep(1)
                            st.session_state.page = "home"
                            st.rerun()
                        else:
                            st.error("❌ Invalid email or password")
                    except Exception as e:
                        st.error(f"❌ Connection error: {str(e)}")
                else:
                    st.warning("⚠️ Please fill all fields")
        
        with col_signin_2:
            if st.button("📝 Create Account", use_container_width=True, key="btn_reg_nav"):
                st.session_state.page = "register"
                st.rerun()
    
    with col_right:
        st.markdown("""
        <div class='card'>
            <h2 class='card-title'>What We Offer</h2>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class='info-card'>
            <div class='info-card-title'>🤖 AI-Powered Learning</div>
            <div class='info-card-desc'>Get unlimited AI-generated quiz questions with instant feedback and detailed explanations tailored to your learning pace.</div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class='info-card'>
            <div class='info-card-title'> Career Development</div>
            <div class='info-card-desc'>Get AI-matched job recommendations, resume analysis, skill gap identification, and personalized roadmaps to reach your career goals.</div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class='info-card'>
            <div class='info-card-title'>🏆 Gamification</div>
            <div class='info-card-desc'>Compete on leaderboards, maintain streaks, earn badges, and celebrate achievements while learning with our community.</div>
        </div>
        """, unsafe_allow_html=True)

# ===== REGISTER PAGE =====

def register_page():
    """Professional Register Page"""
    # Hide sidebar on register page
    st.markdown("""
    <style>
        [data-testid="stSidebar"] { display: none !important; }
    </style>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class='header-main'>
        <h1>🚀 Join Our Community</h1>
        <p>Start Your Learning Journey Today</p>
    </div>
    """, unsafe_allow_html=True)
    
    col_left, col_right = st.columns([1.2, 1])
    
    with col_left:
        st.markdown("""
        <div class='card'>
            <h2 class='card-title'>Create Account</h2>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("### Complete Registration")
        
        email = st.text_input("📧 Email Address", placeholder="your@email.com", key="reg_email")
        username = st.text_input("👤 Username", placeholder="Choose a unique username", key="reg_username")
        password = st.text_input("🔐 Password", type="password", placeholder="Create a strong password", key="reg_pass")
        confirm = st.text_input("🔐 Confirm Password", type="password", placeholder="Confirm your password", key="reg_confirm")
        
        col_reg_1, col_reg_2 = st.columns(2)
        
        with col_reg_1:
            if st.button("✅ Create Account", use_container_width=True, key="btn_create"):
                if not all([email, username, password, confirm]):
                    st.warning("⚠️ Please fill all fields")
                elif password != confirm:
                    st.error("❌ Passwords don't match")
                elif len(password) < 6:
                    st.error("❌ Password must be at least 6 characters")
                else:
                    try:
                        response = requests.post(
                            f"{API_BASE_URL}/auth/register",
                            json={"email": email, "username": username, "password": password},
                            headers=get_headers()
                        )
                        
                        if response.status_code == 200:
                            st.success("✅ Account created! Redirecting...")
                            time.sleep(2)
                            st.session_state.page = "login"
                            st.rerun()
                        else:
                            error_msg = response.json().get('detail', 'Registration failed')
                            st.error(f"❌ {error_msg}")
                    except Exception as e:
                        st.error(f"❌ Error: {str(e)}")
        
        with col_reg_2:
            if st.button("🔙 Back to Login", use_container_width=True, key="btn_back_login"):
                st.session_state.page = "login"
                st.rerun()
    
    with col_right:
        st.markdown("""
        <div class='card'>
            <h2 class='card-title'>Why Join Us?</h2>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class='info-card'>
            <div class='info-card-title'>📚 Comprehensive Learning</div>
            <div class='info-card-desc'>Access 500+ AI-generated questions across Aptitude, Technical, and Core Subjects to strengthen your knowledge base.</div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class='info-card'>
            <div class='info-card-title'>🎯 Personalized Paths</div>
            <div class='info-card-desc'>Get customized learning roadmaps and career development plans tailored specifically to your goals and skill level.</div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class='info-card'>
            <div class='info-card-title'>💼 Job Opportunities</div>
            <div class='info-card-desc'>Receive real-time job recommendations matched to your skills, resume analysis, and interview preparation guidance.</div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class='info-card'>
            <div class='info-card-title'>🏆 Community & Growth</div>
            <div class='info-card-desc'>Join 10,000+ learners, compete on leaderboards, maintain learning streaks, and achieve milestones together.</div>
        </div>
        """, unsafe_allow_html=True)

# ===== HOME PAGE =====

def home_page():
    """Professional Home Page with Project Overview"""
    if not st.session_state.token:
        st.session_state.page = "login"
        st.rerun()
        return
    
    username = st.session_state.user.get('username', 'User') if st.session_state.user else 'User'
    
    st.markdown(f"""
    <div class='header-main'>
        <h1>👋 Welcome Back, {username}!</h1>
        <p>Your personalized AI-powered learning dashboard</p>
    </div>
    """, unsafe_allow_html=True)
    
    # ===== LEARNING DASHBOARD =====
    st.markdown("### 📊 Your Learning Dashboard")
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric(label="📝 Quizzes Taken", value="24", delta="+3 this week")
    with col2:
        st.metric(label="✅ Accuracy Rate", value="78%", delta="+5%")
    with col3:
        st.metric(label="🔥 Current Streak", value="12 days", delta="🔥 Active")
    with col4:
        st.metric(label="🏆 Global Rank", value="#45", delta="⬆ 5 pos")
    
    st.markdown("---")
    
    # ===== QUICK ACTIONS =====
    st.markdown("### ⚡ Quick Actions")
    
    col_qa1, col_qa2, col_qa3, col_qa4 = st.columns(4)
    
    with col_qa1:
        if st.button("📝 Take a Quiz", use_container_width=True, key="qa_quiz"):
            st.session_state.page = "quiz"
            st.rerun()
    with col_qa2:
        if st.button("📄 Analyze Resume", use_container_width=True, key="qa_resume"):
            st.session_state.page = "resume"
            st.rerun()
    with col_qa3:
        if st.button("💼 Find Jobs", use_container_width=True, key="qa_jobs"):
            st.session_state.page = "jobs"
            st.rerun()
    with col_qa4:
        if st.button("🛣️ Learning Path", use_container_width=True, key="qa_roadmap"):
            st.session_state.page = "roadmap"
            st.rerun()
    
    st.markdown("---")
    
    # ===== PROJECT OVERVIEW =====
    st.markdown("### 📚 About This Platform")
    
    st.markdown("""
    <div class='card'>
        <h3>What is AI Training Assistant?</h3>
        <p>AI Training Assistant is a comprehensive learning platform designed to help students and professionals master their skills through AI-powered quizzes, personalized learning paths, resume analysis, and job recommendations. Our mission is to democratize quality education and align learning with industry demands.</p>
    </div>
    """, unsafe_allow_html=True)
    
    # ===== KEY FEATURES DASHBOARD =====
    st.markdown("### 🌟 Our Key Features")
    
    features_data = [
        {"emoji": "📝", "title": "AI Quizzes", "desc": "Unlimited AI-generated questions with instant feedback and explanations"},
        {"emoji": "📊", "title": "Progress Analytics", "desc": "Detailed insights into your learning journey and improvement areas"},
        {"emoji": "🏆", "title": "Leaderboards", "desc": "Compete with learners worldwide and track achievements"},
        {"emoji": "📄", "title": "Resume Analyzer", "desc": "AI-powered resume analysis identifying skill gaps and improvements"},
        {"emoji": "💼", "title": "Job Matching", "desc": "Curated job opportunities aligned with your skills and goals"},
        {"emoji": "🛣️", "title": "Learning Roadmaps", "desc": "Personalized career development paths with milestone tracking"},
    ]
    
    cols = st.columns(3)
    for idx, feature in enumerate(features_data):
        with cols[idx % 3]:
            st.markdown(f"""
            <div class='feature-card'>
                <div class='feature-icon'>{feature['emoji']}</div>
                <div class='feature-name'>{feature['title']}</div>
                <div class='feature-desc'>{feature['desc']}</div>
            </div>
            """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # ===== QUIZ CATEGORIES =====
    st.markdown("### 📖 Quiz Categories Available")
    
    col_cat1, col_cat2, col_cat3 = st.columns(3)
    
    with col_cat1:
        st.markdown("""
        <div class='card'>
            <h3>📚 Aptitude</h3>
            <p style='color: #1a7aac;'>✓ Quantitative Analysis<br>✓ Logical Reasoning<br>✓ English Language<br>✓ Data Interpretation</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col_cat2:
        st.markdown("""
        <div class='card'>
            <h3>💻 Technical</h3>
            <p style='color: #1a7aac;'>✓ Python Programming<br>✓ JavaScript & Web<br>✓ Java & OOP<br>✓ DSA & Algorithms</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col_cat3:
        st.markdown("""
        <div class='card'>
            <h3>🔧 Core Subjects</h3>
            <p style='color: #1a7aac;'>✓ Operating Systems<br>✓ Database Management<br>✓ Computer Networks<br>✓ System Design</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # ===== PLATFORM STATISTICS =====
    st.markdown("### 📊 Platform Statistics")
    
    stat_cols = st.columns(5)
    
    stats = [
        {"value": "500+", "label": "Quiz Questions"},
        {"value": "50+", "label": "Job Postings"},
        {"value": "10000+", "label": "Active Users"},
        {"value": "95%", "label": "Success Rate"},
        {"value": "24/7", "label": "Support"},
    ]
    
    for col, stat in zip(stat_cols, stats):
        with col:
            st.markdown(f"""
            <div class='feature-card' style='text-align: center;'>
                <div style='font-size: 2rem; font-weight: 800; color: #64B5F6; margin: 10px 0;'>{stat['value']}</div>
                <div style='font-size: 0.9rem; color: #1a7aac;'>{stat['label']}</div>
            </div>
            """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # ===== WEEKLY ACTIVITY CHART =====
    st.markdown("### 📈 Your Weekly Activity")
    
    activity_data = {
        'Day': ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'],
        'Quizzes Attempted': [5, 7, 3, 8, 6, 9, 4]
    }
    
    df = pd.DataFrame(activity_data)
    
    fig = px.bar(
        df, x='Day', y='Quizzes Attempted',
        title="Quiz Attempts This Week",
        color='Quizzes Attempted',
        color_continuous_scale=['#1565c0', '#2196F3', '#64B5F6']
    )
    
    fig.update_layout(
        plot_bgcolor='rgba(25, 55, 95, 0.3)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color='#e3f2fd', size=12),
        xaxis=dict(showgrid=True, gridwidth=1, gridcolor='rgba(255, 255, 255, 0.1)'),
        yaxis=dict(showgrid=True, gridwidth=1, gridcolor='rgba(255, 255, 255, 0.1)'),
        hovermode='x unified'
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("---")
    
    # ===== ACHIEVEMENTS =====
    st.markdown("### 🏆 Your Achievements")
    
    ach_cols = st.columns(3)
    
    achievements = [
        {"emoji": "🔥", "title": "12-Day Streak", "desc": "Keep your learning momentum!"},
        {"emoji": "🎯", "title": "Expert Achiever", "desc": "50+ quizzes with 80%+ accuracy"},
        {"emoji": "⭐", "title": "Rising Star", "desc": "Climbed 10 positions"},
    ]
    
    for col, achievement in zip(ach_cols, achievements):
        with col:
            st.markdown(f"""
            <div class='feature-card'>
                <div class='feature-icon'>{achievement['emoji']}</div>
                <div class='feature-name'>{achievement['title']}</div>
                <div class='feature-desc'>{achievement['desc']}</div>
            </div>
            """, unsafe_allow_html=True)

# ===== QUIZ PAGE =====

def quiz_page():
    """Quiz Page"""
    st.markdown("""
    <div class='header-main'>
        <h1>📝 AI Quiz Generator</h1>
        <p>Test Your Knowledge with Intelligent Questions</p>
    </div>
    """, unsafe_allow_html=True)
    
    col_settings, col_questions = st.columns([1, 2.5])
    
    with col_settings:
        st.markdown("""
        <div class='card'>
            <h2 class='card-title'>Quiz Settings</h2>
        </div>
        """, unsafe_allow_html=True)
        
        category = st.selectbox("📚 Category", ["Aptitude", "Technical", "Core Subjects"])
        subcategory_map = {
            "Aptitude": ["Quantitative", "Logical Reasoning", "English"],
            "Technical": ["Python", "JavaScript", "Java", "C++", "DSA"],
            "Core Subjects": ["Operating Systems", "DBMS", "Networks"],
        }
        subcategory = st.selectbox("🎯 Subcategory", subcategory_map.get(category, []))
        difficulty = st.select_slider("⭐ Difficulty Level", options=["Easy", "Medium", "Hard"])
        num_questions = st.slider("❓ Number of Questions", 5, 50, 10, 5)
        
        if st.button("🚀 Generate Quiz", use_container_width=True):
            st.success(f"✅ Quiz generated with {num_questions} questions!")
    
    with col_questions:
        st.markdown("""
        <div class='card'>
            <h2 class='card-title'>Sample Question</h2>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("**Question 1 of 10**")
        st.markdown("**If a train travels 100 km in 2 hours, what is its speed?**")
        
        answer = st.radio("Select answer:", ["A) 25 km/h", "B) 50 km/h", "C) 75 km/h", "D) 100 km/h"])
        
        col_nav1, col_nav2 = st.columns(2)
        with col_nav1:
            st.button("⏭️ Next Question", use_container_width=True)
        with col_nav2:
            st.button("✅ Submit Answer", use_container_width=True)

# ===== RESUME PAGE =====

def resume_page():
    """Resume Analysis Page"""
    st.markdown("""
    <div class='header-main'>
        <h1>📄 Resume Analyzer</h1>
        <p>Extract Skills & Identify Development Areas</p>
    </div>
    """, unsafe_allow_html=True)
    
    col_upload, col_results = st.columns([1, 2])
    
    with col_upload:
        st.markdown("""
        <div class='card'>
            <h2 class='card-title'>Upload Resume</h2>
        </div>
        """, unsafe_allow_html=True)
        
        uploaded_file = st.file_uploader("Choose resume (PDF/TXT)", type=["pdf", "txt"])
        
        if uploaded_file:
            st.success(f"✅ {uploaded_file.name} uploaded")
            if st.button("🔍 Analyze Resume", use_container_width=True):
                st.info("Analyzing...")
                time.sleep(2)
                st.success("Analysis complete!")
    
    with col_results:
        st.markdown("""
        <div class='card'>
            <h2 class='card-title'>Analysis Results</h2>
        </div>
        """, unsafe_allow_html=True)
        
        col_r1, col_r2 = st.columns(2)
        with col_r1:
            st.metric("Experience", "3 Years")
        with col_r2:
            st.metric("Skills Found", "8")

# ===== JOBS PAGE =====

def jobs_page():
    """Jobs Page"""
    st.markdown("""
    <div class='header-main'>
        <h1>💼 Job & Internship Opportunities</h1>
        <p>Find Roles Matched to Your Skills</p>
    </div>
    """, unsafe_allow_html=True)
    
    col_filter, col_jobs = st.columns([1, 3])
    
    with col_filter:
        st.markdown("""
        <div class='card'>
            <h2 class='card-title'>Filters</h2>
        </div>
        """, unsafe_allow_html=True)
        
        search = st.text_input("🔍 Search", placeholder="Python, React...")
        location = st.text_input("📍 Location", placeholder="Remote, India")
        job_type = st.selectbox("💼 Type", ["All", "Full-time", "Internship"])
        
        if st.button("Apply Filters", use_container_width=True):
            st.success("Filters applied!")
    
    with col_jobs:
        st.markdown("""
        <div class='card'>
            <h2 class='card-title'>Recommended For You</h2>
        </div>
        """, unsafe_allow_html=True)
        
        jobs = [
            {"title": "Senior Python Developer", "company": "Google", "match": "95%"},
            {"title": "React Developer", "company": "Meta", "match": "88%"},
            {"title": "Full Stack Developer", "company": "Amazon", "match": "82%"},
        ]
        
        for job in jobs:
            st.markdown(f"""
            <div class='info-card' style='border-left: 4px solid #2196F3;'>
                <div class='info-card-title'>{job['title']}</div>
                <div class='info-card-desc'><strong>{job['company']}</strong> | Match: {job['match']}</div>
            </div>
            """, unsafe_allow_html=True)

# ===== ROADMAP PAGE =====

def roadmap_page():
    """Learning Roadmap Page"""
    st.markdown("""
    <div class='header-main'>
        <h1>🛣️ Personalized Learning Roadmap</h1>
        <p>Your Path to Career Goals</p>
    </div>
    """, unsafe_allow_html=True)
    
    col_create, col_plan = st.columns([1, 2])
    
    with col_create:
        st.markdown("""
        <div class='card'>
            <h2 class='card-title'>Create Roadmap</h2>
        </div>
        """, unsafe_allow_html=True)
        
        current = st.text_input("Current Role", value="Junior Developer")
        target = st.text_input("Target Role", value="Senior Full Stack Developer")
        
        if st.button("🗺️ Generate Roadmap", use_container_width=True):
            st.success("Roadmap created!")
            st.session_state.roadmap_gen = True
    
    with col_plan:
        if st.session_state.get("roadmap_gen", False):
            st.markdown("""
            <div class='card'>
                <h2 class='card-title'>Your 6-Month Plan</h2>
            </div>
            """, unsafe_allow_html=True)
            
            months = [
                ("Month 1: Docker & Kubernetes", 25),
                ("Month 2: AWS & Cloud", 40),
                ("Month 3: CI/CD Pipeline", 60),
                ("Month 4: Microservices", 75),
                ("Month 5: System Design", 85),
                ("Month 6: Portfolio", 100),
            ]
            
            for month, progress in months:
                st.write(month)
                st.progress(progress / 100)

# ===== LEADERBOARD PAGE =====

def leaderboard_page():
    """Leaderboard Page"""
    st.markdown("""
    <div class='header-main'>
        <h1>🏆 Leaderboards & Achievements</h1>
        <p>See How You Rank Among Learners</p>
    </div>
    """, unsafe_allow_html=True)
    
    lb_type = st.selectbox("📊 Leaderboard Type", ["Global", "Category", "Weekly"])
    
    st.markdown("---")
    
    leaderboard_data = {
        "Rank": [1, 2, 3, 4, 5],
        "User": ["Alice Chen", "Bob Kumar", "Charlie Brown", "Diana Prince", "Your Name"],
        "Points": [4850, 4620, 4390, 4210, 3950],
        "Quizzes": [156, 148, 142, 135, 128],
        "Accuracy": ["94%", "91%", "88%", "85%", "78%"]
    }
    
    df = pd.DataFrame(leaderboard_data)
    st.dataframe(df, use_container_width=True, hide_index=True)
    
    st.markdown("---")
    
    col_l1, col_l2, col_l3, col_l4 = st.columns(4)
    with col_l1:
        st.metric("Your Rank", "#5")
    with col_l2:
        st.metric("Points", "3950")
    with col_l3:
        st.metric("Streak", "12 days")
    with col_l4:
        st.metric("Accuracy", "78%")

# ===== MAIN NAVIGATION =====

def main():
    if not hasattr(st.session_state, 'page'):
        st.session_state.page = 'home' if st.session_state.token else 'login'
    
    # Sidebar Navigation
    if st.session_state.token:
        st.sidebar.markdown("""
        <div style='text-align: center; padding: 25px 15px; margin-bottom: 30px;'>
            <h1 style='color: #ffffff; font-size: 2rem; margin: 0; font-weight: 900;'>🎓</h1>
            <h2 style='color: #ffffff; font-size: 1.3rem; margin: 10px 0 5px 0; font-weight: 700;'>AI Training</h2>
            <p style='color: rgba(255,255,255,0.7); font-size: 0.8rem; margin: 0;'>Assistant</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.sidebar.markdown("---")
        
        st.sidebar.markdown("<p style='color: #ffffff; font-weight: 700; padding: 10px 0;'>NAVIGATION</p>", unsafe_allow_html=True)
        
        pages_map = {
            "🏠 Home": "home",
            "📝 Quiz": "quiz",
            "📄 Resume": "resume",
            "💼 Jobs": "jobs",
            "🛣️ Roadmap": "roadmap",
            "🏆 Leaderboard": "leaderboard",
        }
        
        selected = st.sidebar.radio("", list(pages_map.keys()), key="nav_radio", label_visibility="collapsed")
        st.session_state.page = pages_map[selected]
        
        st.sidebar.markdown("---")
        
        if st.sidebar.button("🚪 LOGOUT", use_container_width=True, key="btn_logout"):
            st.session_state.token = None
            st.session_state.user = None
            st.session_state.page = "login"
            st.success("✅ Logged out successfully!")
            st.rerun()
    
    # Route to pages
    if st.session_state.page == "login":
        login_page()
    elif st.session_state.page == "register":
        register_page()
    elif st.session_state.page == "home":
        home_page()
    elif st.session_state.page == "quiz":
        quiz_page()
    elif st.session_state.page == "resume":
        resume_page()
    elif st.session_state.page == "jobs":
        jobs_page()
    elif st.session_state.page == "roadmap":
        roadmap_page()
    elif st.session_state.page == "leaderboard":
        leaderboard_page()

if __name__ == "__main__":
    main()
