import streamlit as st

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
