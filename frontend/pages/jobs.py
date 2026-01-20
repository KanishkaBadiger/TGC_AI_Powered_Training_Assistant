# frontend/pages/jobs.py
import streamlit as st
import requests
import os

def jobs_page():
    """Jobs Page"""
    st.set_page_config(page_title="Job & Internship Finder", layout="wide")

    # Backend URL
    API_URL = "http://localhost:8000/api/jobs/search"

    st.markdown("""
    <div class='header-main'>
        <h1>💼 Job & Internship Opportunities</h1>
        <p>Find Roles Matched to Your Skills</p>
    </div>
    """, unsafe_allow_html=True)

    # --- Custom CSS for Job Cards ---
    st.markdown("""
    <style>
        .job-card {
            background-color: #ffffff;
            padding: 20px;
            border-radius: 10px;
            border: 1px solid #e0e0e0;
            margin-bottom: 15px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.05);
            transition: transform 0.2s;
        }
        .job-card:hover {
            transform: translateY(-2px);
            box-shadow: 0 4px 8px rgba(0,0,0,0.1);
        }
        .job-title {
            color: #2c3e50;
            font-size: 1.2rem;
            font-weight: bold;
            margin-bottom: 5px;
        }
        .company-name {
            color: #7f8c8d;
            font-weight: 600;
            margin-bottom: 10px;
        }
        .tags {
            display: inline-block;
            background-color: #f0f2f6;
            padding: 2px 8px;
            border-radius: 4px;
            font-size: 0.8rem;
            color: #555;
            margin-right: 10px;
            margin-bottom: 8px;
        }
        .apply-btn {
            background-color: #23b5d3;
            color: white;
            padding: 8px 15px;
            text-decoration: none;
            border-radius: 5px;
            font-weight: bold;
            display: inline-block;
            margin-top: 10px;
        }
        .apply-btn:hover {
            background-color: #1a8a9f;
            color: white;
        }
    </style>
    """, unsafe_allow_html=True)

    st.title("🔎 What are you looking for?")
    # st.caption("Find the latest opportunities tailored to your profile.")

    # --- 🔍 SEARCH INPUTS (New 3-Column Layout) ---
    # st.markdown("### 🔎 What are you looking for?")

    col1, col2, col3 = st.columns([2, 1, 1])

    with col1:
        target_role = st.text_input(
            "Job Role / Skill", 
            placeholder="e.g. Python Developer, Data Analyst",
            value=""
        )

    with col2:
        job_type = st.selectbox(
            "Opportunity Type",
            ["Internship", "Full-time Job", "Part-time", "Freelance"],
            index=0 # Default to Internship
        )

    with col3:
        target_location = st.text_input(
            "Location", 
            value="India", 
            placeholder="City or 'Remote'"
        )

    # Search Button (Full Width)
    search_clicked = st.button("🔍 Find Opportunities", type="primary", use_container_width=True)

    st.markdown("---")

    # --- LOGIC ---
    if search_clicked:
        if not target_role:
            st.warning("⚠️ Please enter a Job Role (e.g. 'Web Developer')")
        else:
            # Construct a smart search query
            # e.g. "Python Developer Internship"
            final_query = f"{target_role} {job_type}"
            
            with st.spinner(f"Searching for **{final_query}** in **{target_location}**..."):
                try:
                    # Call Backend
                    params = {
                        "query": final_query,
                        "location": target_location
                    }
                    
                    response = requests.get(API_URL, params=params)
                    
                    if response.status_code == 200:
                        data = response.json()
                        jobs = data.get("jobs", [])
                        
                        st.markdown(f"### Found {len(jobs)} {job_type}s")
                        
                        if len(jobs) == 0:
                            st.info("No results found. Try changing the location or role keywords.")
                        
                        for job in jobs:
                            # Render Job Card
                            st.markdown(f"""
                            <div class="job-card">
                                <div class="job-title">{job['title']}</div>
                                <div class="company-name">
                                    🏢 {job['company']} 
                                </div>
                                <div>
                                    <span class="tags">📍 {target_location}</span>
                                    <span class="tags">📅 {job['date']}</span>
                                    <span class="tags">💼 {job_type}</span>
                                </div>
                                <div style="color: #555; font-size: 0.95rem; margin-top: 10px; margin-bottom: 10px;">
                                    {job['snippet']}
                                </div>
                                <a href="{job['link']}" target="_blank" class="apply-btn">Apply Now ↗</a>
                            </div>
                            """, unsafe_allow_html=True)
                            
                    else:
                        st.error(f"Search failed. Error: {response.text}")
                        
                except Exception as e:
                    st.error(f"Connection Error: {str(e)}")

    # --- Default State (Instructions) ---
    if not search_clicked:
        st.info("💡 **Tip:** Select 'Internship' to find freshers' roles specifically!")