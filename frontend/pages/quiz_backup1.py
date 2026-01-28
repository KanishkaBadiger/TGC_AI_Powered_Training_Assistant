import streamlit as st
import requests
import time 

# --- PAGE CONFIG ---
st.set_page_config(page_title="AI Skill Assessment", page_icon="📝", layout="wide")


# We assume user is logged in, but use .get() to prevent crashes if session is empty
USER = st.session_state.get('user', {"id": None, "username": "Guest"})

API_URL = "http://localhost:8000/api/quiz"

def quiz_page():
    """Quiz Page"""
    st.markdown("""
    <div class='header-main'>
        <h1>📝 AI Skill Assessment Center</h1>
        <p>Generate Customized Quizzes to Test and Improve Your Skills</p>
    </div>
    """, unsafe_allow_html=True)
    # --- CUSTOM CSS ---

    TOPICS = {
        "Aptitude Round": ["Quantitative Aptitude", "Logical Reasoning", "Verbal Ability"],
        "Technical Round": ["Python", "Java", "C++", "Data Structures (DSA)", "SQL", "JavaScript"],
        "Core Subjects": ["Operating Systems (OS)", "DBMS", "Computer Networks", "OOPs Concepts"],
        "Full Mock": ["Mixed Aptitude & Technical"]
    }

    # --- CSS STYLING (Professional Orange Theme) ---
    st.markdown("""
    <style>
        .stApp { background-color: #f8f9fa; }
        
        /* Config Card */
        .config-card {
            background: white; padding: 25px; border-radius: 12px;
            box-shadow: 0 4px 15px rgba(0,0,0,0.05); border-top: 5px solid #fd7e14;
            margin-bottom: 20px;
        }
        
        /* Question Card */
        .q-card {
            background: white; padding: 20px; border-radius: 10px;
            border: 1px solid #e9ecef; margin-bottom: 15px;
        }
        
        /* Answer States */
        .correct-box { background: #d1e7dd; color: #0f5132; padding: 15px; border-radius: 8px; border-left: 5px solid #198754; margin-top: 10px; }
        .wrong-box { background: #f8d7da; color: #842029; padding: 15px; border-radius: 8px; border-left: 5px solid #dc3545; margin-top: 10px; }
        
        /* Custom Buttons */
        div.stButton > button {
            width: 100%; border-radius: 6px; font-weight: 600; padding: 0.6rem;
        }
        /* Orange Primary Button override */
        button[kind="primary"] {
            background-color: #fd7e14 !important; border-color: #fd7e14 !important;
        }
        button[kind="primary"]:hover {
            background-color: #e36a0e !important; border-color: #e36a0e !important;
        }
    </style>
    """, unsafe_allow_html=True)

    # --- STATE MANAGEMENT ---
    if 'quiz_state' not in st.session_state: st.session_state.quiz_state = "SETUP" # SETUP, ACTIVE, RESULT
    if 'quiz_data' not in st.session_state: st.session_state.quiz_data = []
    if 'user_answers' not in st.session_state: st.session_state.user_answers = {}
    if 'start_time' not in st.session_state: st.session_state.start_time = None

    # =========================================================
    # PHASE 1: TEST CONFIGURATION (Dashboard)
    # =========================================================
    if st.session_state.quiz_state == "SETUP":
        st.title("🎓 Interview Mock Test Lab")
        st.markdown(f"Hi **{USER['username']}**, configure your practice session below.")
        
        st.markdown('<div class="config-card">', unsafe_allow_html=True)
        
        # 1. Layout Columns
        col1, col2 = st.columns(2)
        
        with col1:
            # Category Selector (Triggers Refresh)
            selected_cat = st.selectbox("Select Interview Round", list(TOPICS.keys()))
            
            # Sub-Category (Dynamic)
            available_subs = TOPICS[selected_cat]
            selected_sub = st.selectbox("Select Specific Topic", available_subs)

        with col2:
            selected_diff = st.selectbox("Difficulty Level", ["Beginner (Fresher)", "Intermediate", "Advanced"])
            selected_count = st.slider("Number of Questions", 5, 20, 10)

        st.markdown("<br>", unsafe_allow_html=True)
        
        if st.button("🚀 Start Mock Test", type="primary"):
            with st.spinner("🤖 AI is curating unique interview questions..."):
                try:
                    payload = {
                        "category": selected_cat,
                        "sub_category": selected_sub,
                        "difficulty": selected_diff,
                        "num_questions": selected_count
                    }
                    # Call Backend
                    res = requests.post(f"{API_URL}/generate", json=payload)
                    
                    if res.status_code == 200:
                        st.session_state.quiz_data = res.json()['questions']
                        st.session_state.user_answers = {} # Reset answers
                        st.session_state.quiz_state = "ACTIVE" # Switch Mode
                        st.session_state.current_params = payload # Save context
                        st.session_state.start_time = time.time()
                        st.rerun()
                    else:
                        st.error("⚠️ AI Service Busy. Please try again in a few seconds.")
                except Exception as e:
                    st.error(f"❌ Connection Failed: {e}")
                    
        st.markdown('</div>', unsafe_allow_html=True)

    # =========================================================
    # PHASE 2: ACTIVE TEST
    # =========================================================
    elif st.session_state.quiz_state == "ACTIVE":
        st.title("📝 Mock Test In Progress")
        
        questions = st.session_state.quiz_data
        total_q = len(questions)
        
        # Progress Bar
        answered_count = len(st.session_state.user_answers)
        st.progress(answered_count / total_q)
        
        with st.form("quiz_form"):
            for i, q in enumerate(questions):
                st.markdown(f"""
                <div class="q-card">
                    <h5 style="margin-bottom:10px;">Q{i+1}: {q['question']}</h5>
                </div>
                """, unsafe_allow_html=True)
                
                # Radio Buttons for Options
                st.session_state.user_answers[i] = st.radio(
                    "Select Answer:",
                    q['options'],
                    key=f"q_{i}",
                    index=None, # Default to nothing selected
                    label_visibility="collapsed"
                )
            
            st.markdown("---")
            submit_btn = st.form_submit_button("✅ Submit Test", type="primary")
            
            if submit_btn:
                st.session_state.quiz_state = "RESULT"
                st.rerun()

    # =========================================================
    # PHASE 3: RESULT & ANALYSIS
    # =========================================================
    elif st.session_state.quiz_state == "RESULT":
        st.title("📊 Test Performance Report")
        
        questions = st.session_state.quiz_data
        answers = st.session_state.user_answers
        
        # Calculate Score
        score = 0
        for i, q in enumerate(questions):
            if answers.get(i) == q['correct_option']:
                score += 1
        
        percentage = (score / len(questions)) * 100
        
        # Display Score Card
        st.markdown('<div class="config-card">', unsafe_allow_html=True)
        c1, c2, c3 = st.columns([1, 2, 1])
        with c2:
            st.metric("Final Score", f"{score} / {len(questions)}", f"{percentage:.1f}%")
            if percentage >= 70:
                st.success("🌟 Great Job! You are ready for this topic.")
            else:
                st.warning("📉 Keep Practicing. Review the explanations below.")
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Detailed Review
        st.subheader("🔍 Detailed Solutions")
        
        for i, q in enumerate(questions):
            user_ans = answers.get(i, "Not Answered")
            correct = q['correct_option']
            is_correct = (user_ans == correct)
            
            icon = "✅" if is_correct else "❌"
            
            with st.expander(f"{icon} Q{i+1}: {q['question']}", expanded=not is_correct):
                if is_correct:
                    st.markdown(f"""<div class="correct-box">
                        <b>Your Answer:</b> {user_ans}<br>
                        <b>💡 Explanation:</b> {q['explanation']}
                    </div>""", unsafe_allow_html=True)
                else:
                    st.markdown(f"""<div class="wrong-box">
                        <b>Your Answer:</b> {user_ans}<br>
                        <b>✅ Correct Answer:</b> {correct}<br><br>
                        <b>💡 Explanation:</b> {q['explanation']}
                    </div>""", unsafe_allow_html=True)

        # Retry Button
        if st.button("🔄 Start New Test"):
            st.session_state.quiz_state = "SETUP"
            st.session_state.quiz_data = []
            st.session_state.user_answers = {}
            st.rerun()