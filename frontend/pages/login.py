import streamlit as st
import requests
import time
from api import get_headers
from config import API_BASE_URL

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
        <h1>🎓 AI Powered Training Assistant</h1>
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
        
                            # ✅ SAVE USER DATA TO SESSION STATE
                            st.session_state['token'] = data['access_token']
                            st.session_state['user'] = data['user']  # <--- THIS IS CRITICAL
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