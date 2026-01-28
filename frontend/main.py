import streamlit as st
import requests
import json
from datetime import datetime
import pandas as pd
import time
import plotly.graph_objects as go
import plotly.express as px

from utils.styles import load_styles

from pages.login import login_page
from pages.register import register_page
from pages.quiz import quiz_page
from pages.resume import resume_page
from pages.jobs import jobs_page
from pages.roadmap import roadmap_page
from pages.leaderboard import leaderboard_page

load_styles()

# Configure page
st.set_page_config(
    page_title="AI Training Assistant",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# API Configuration
# API_BASE_URL = "http://localhost:8000/api/v1"

def init_session_state():
    """Initialize session state"""
    if "token" not in st.session_state:
        st.session_state.token = None
    if "user" not in st.session_state:
        st.session_state.user = None
    if "page" not in st.session_state:
        st.session_state.page = "login"

init_session_state()

# ===== LOGIN PAGE =====
# ===== REGISTER PAGE =====
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
        st.metric(label="🔥 Current Streak", value="07 days", delta="🔥 Active")
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
        {"emoji": "📄", "title": "Resume Analyzer", "desc": "AI-powered resume analysis identifying skill gaps and improvements"},
        {"emoji": "💼", "title": "Job Matching", "desc": "Curated job opportunities aligned with your skills and goals"},
        {"emoji": "🛣️", "title": "Learning Roadmaps", "desc": "Personalized career development paths with milestone tracking"},
        {"emoji": "🏆", "title": "Leaderboards", "desc": "Compete with learners worldwide and track achievements"},
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
        {"value": "50+", "label": "Quiz Questions"},
        {"value": "50+", "label": "Job Postings"},
        {"value": "1000+", "label": "Active Users"},
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
        {"emoji": "🔥", "title": "07-Day Streak", "desc": "Keep your learning momentum!"},
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

# ===== RESUME PAGE =====

# ===== JOBS PAGE =====

# ===== ROADMAP PAGE =====

# ===== LEADERBOARD PAGE =====

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
            <h4 style='color: rgba(255,255,255,0.7); font-size: 0.8rem; margin: 0;'>Assistant</h4>
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
        
        # selected = st.sidebar.radio("", list(pages_map.keys()), key="nav_radio", label_visibility="collapsed")
        selected = st.sidebar.radio(
            "Navigation",
            list(pages_map.keys()),
            key="nav_radio",
            label_visibility="collapsed"
        )

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
