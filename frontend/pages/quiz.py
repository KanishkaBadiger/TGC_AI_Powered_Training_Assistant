import streamlit as st

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
