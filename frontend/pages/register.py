import streamlit as st
import requests
import time
from api import get_headers
from config import API_BASE_URL

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