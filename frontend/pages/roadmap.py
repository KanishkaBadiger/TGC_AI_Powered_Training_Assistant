import streamlit as st

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