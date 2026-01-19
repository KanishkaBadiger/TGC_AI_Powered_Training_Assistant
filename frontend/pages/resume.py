import streamlit as st
import requests
import json
import time
from datetime import datetime
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import os

# Get API base URL from secrets or environment variable or use default
try:
    API_BASE_URL = st.secrets.get("API_BASE_URL", os.getenv("API_BASE_URL", "http://localhost:8000/api"))
except Exception:
    API_BASE_URL = os.getenv("API_BASE_URL", "http://localhost:8000/api")

# Get auth token from session
def get_auth_headers():
    """Get authorization headers"""
    token = st.session_state.get('token', '')
    headers = {}
    if token:
        headers['Authorization'] = f'Bearer {token}'
    return headers

def resume_page():
    """Complete Resume Analysis System with Detailed Output"""
    # <div style='background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 30px; border-radius: 10px; color: white; margin-bottom: 20px;'>
    st.markdown("""       
    <div class='header-main'>
        <h1>📄 Advanced Resume Analyzer</h1>
        <p style='font-size: 1.1rem;'>AI-Powered Resume Analysis with Role Matching, Scoring & Interview Prep</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Initialize session state
    if "resume_id" not in st.session_state:
        st.session_state.resume_id = None
    if "resume_text" not in st.session_state:
        st.session_state.resume_text = None
    if "job_description" not in st.session_state:
        st.session_state.job_description = None
    if "target_role" not in st.session_state:
        st.session_state.target_role = None
    if "role_matching_done" not in st.session_state:
        st.session_state.role_matching_done = False
    if "analysis_results" not in st.session_state:
        st.session_state.analysis_results = {}
    if "token" not in st.session_state:
        st.session_state.token = None
    
    # Custom styling
    st.markdown("""
    <style>
    .stTabs [data-baseweb="tab-list"] button [data-testid="stMarkdownContainer"] p {
        font-size: 1.2rem !important;
        font-weight: 600 !important;
    }
    .stTabs [data-baseweb="tab-list"] button {
        padding: 15px 25px !important;
        gap: 10px !important;
    }
    .card {
        background-color: #f8f9fa;
        padding: 20px;
        border-radius: 10px;
        border-left: 5px solid #23b5d3;
        margin-bottom: 15px;
    }
    .score-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 25px;
        border-radius: 10px;
        text-align: center;
        margin: 10px 0;
    }
    </style>
    """, unsafe_allow_html=True)
    
    tabs = st.tabs([
        "📤 Upload Resume",
        "🎯 Role Matching",
        "⭐ Resume Score",
        "🔍 Skill Gap",
        "📚 Upskilling",
        "🎤 Interview Prep"
    ])
    
    # ==================== TAB 1: UPLOAD RESUME ====================
    with tabs[0]:
        st.markdown("""
        <div class='card'>
            <h2>📤 Upload Your Resume</h2>
            <p>Supported formats: <b>PDF, DOC, DOCX, TXT</b></p>
        </div>
        """, unsafe_allow_html=True)
        
        st.write("Upload your resume to get started with AI-powered analysis. Choose from PDF, DOC, DOCX, or TXT format.")
        
        uploaded_file = st.file_uploader(
            "Choose a resume file",
            type=["pdf", "doc", "docx", "txt"],
            key="resume_upload",
            help="Supported formats: PDF, DOC, DOCX, TXT"
        )
        
        if uploaded_file:
            st.success(f"✅ File selected: {uploaded_file.name}")
            
            with st.spinner("📄 Uploading your resume..."):
                try:
                    files = {"file": (uploaded_file.name, uploaded_file)}
                    headers = get_auth_headers()
                    
                    response = requests.post(
                        f"{API_BASE_URL}/resume/upload",
                        files=files,
                        headers=headers
                    )
                    
                    if response.status_code == 200:
                        data = response.json()
                        st.session_state.resume_id = data.get("resume_id")
                        st.session_state.resume_text = data.get("resume_text")
                        
                        st.success("✅ Resume uploaded successfully!")
                        st.balloons()
                        
                        # Display resume info
                        col_info1, col_info2 = st.columns(2)
                        with col_info1:
                            st.metric("Resume ID", st.session_state.resume_id)
                        with col_info2:
                            resume_length = len(st.session_state.resume_text) if st.session_state.resume_text else 0
                            st.metric("Text Length", f"{resume_length} characters")
                        
                        # Display resume preview
                        if st.session_state.resume_text:
                            with st.expander("📋 Preview Uploaded Resume"):
                                preview_text = st.session_state.resume_text[:1500]
                                if len(st.session_state.resume_text) > 1500:
                                    preview_text += "\n\n... (truncated for preview)"
                                st.text(preview_text)
                        
                        st.info("✨ Resume ready! Proceed to '🎯 Role Matching' tab to start your analysis.")
                    else:
                        st.error(f"❌ Upload failed: {response.text}")
                except Exception as e:
                    st.error(f"❌ Error: {str(e)}")
        else:
            st.info("👆 Please upload a resume file to get started")
    
    # ==================== TAB 2: ROLE MATCHING ====================
    with tabs[1]:
        st.markdown("""
        <div class='card'>
            <h2>🎯 Role Matching Analysis</h2>
            <p>Select a role and provide job description for accurate analysis</p>
        </div>
        """, unsafe_allow_html=True)
        
        if not st.session_state.resume_id:
            st.error("❌ **Please upload your resume first in the 'Upload Resume' tab**")
        else:
            # Step 1: Select target role
            st.markdown("### Step 1️⃣: Select Target Role")
            
            roles = {
                "Senior Python Developer": "5+ years Python, Django/FastAPI, PostgreSQL, Docker, Kubernetes",
                "Full Stack Developer": "Frontend: React/Vue, Backend: Node/Python, Databases, APIs",
                "DevOps Engineer": "Kubernetes, Docker, CI/CD, AWS/Azure/GCP, Infrastructure",
                "Data Scientist": "Python, ML/AI, Statistics, SQL, Data Visualization",
                "Cloud Architect": "AWS/Azure/GCP, Microservices, Security, High Availability",
                "Custom Role": "Specify your own role and requirements"
            }
            
            selected_role = st.selectbox(
                "Select target role",
                list(roles.keys()),
                help="Choose a role to match your resume against"
            )
            
            col_role1, col_role2 = st.columns(2)
            with col_role1:
                st.success(f"✅ Selected: {selected_role}")
            with col_role2:
                st.write(f"*{roles[selected_role]}*")
            
            st.markdown("---")
            
            # Step 2: Enter job description
            st.markdown("### Step 2️⃣: Enter Job Description")
            st.write("**Provide detailed job description for more accurate analysis. The more detailed, the better the results!**")
            
            job_description = st.text_area(
                "Job Description",
                height=250,
                placeholder="Paste the complete job description here...\n\nExample:\nSenior Python Developer\nRequirements:\n- 5+ years Python experience\n- FastAPI/Django frameworks\n- PostgreSQL, Redis\n- Docker and Kubernetes\n...",
                key="job_desc"
            )
            
            target_role = selected_role if selected_role != "Custom Role" else "Custom Role"
            
            if st.button("🔍 Analyze Match", use_container_width=True, type="primary"):
                if not job_description.strip() or len(job_description) < 50:
                    st.error("❌ Please enter a detailed job description (minimum 50 characters)")
                else:
                    with st.spinner("🔄 Analyzing your resume against job requirements..."):
                        try:
                            st.session_state.job_description = job_description
                            st.session_state.target_role = target_role
                            
                            headers = get_auth_headers()
                            payload = {
                                "resume_id": st.session_state.resume_id,
                                "job_description": job_description,
                                "target_role": target_role
                            }
                            
                            response = requests.post(
                                f"{API_BASE_URL}/resume/role-matching",
                                json=payload,
                                headers=headers
                            )
                            
                            if response.status_code == 200:
                                data = response.json()
                                st.session_state.analysis_results['role_matching'] = data
                                st.session_state.role_matching_done = True
                                
                                st.success("✅ Analysis Complete!")
                                st.balloons()
                                
                                # Match score display
                                col_m1, col_m2 = st.columns(2)
                                
                                with col_m1:
                                    match_pct = data.get("match_percentage", 0)
                                    fig = go.Figure(data=[
                                        go.Indicator(
                                            mode="gauge+number",
                                            value=match_pct,
                                            title={"text": "Match %"},
                                            gauge={
                                                "axis": {"range": [0, 100]},
                                                "bar": {"color": "#23b5d3"},
                                                "steps": [
                                                    {"range": [0, 50], "color": "#f0f4f8"},
                                                    {"range": [50, 75], "color": "#e8f4f8"},
                                                    {"range": [75, 100], "color": "#d4e8f0"}
                                                ]
                                            }
                                        )
                                    ])
                                    fig.update_layout(height=300)
                                    st.plotly_chart(fig, use_container_width=True)
                                
                                with col_m2:
                                    st.markdown("""
                                    <div class='card'>
                                        <h3>📋 Assessment</h3>
                                    </div>
                                    """, unsafe_allow_html=True)
                                    st.write(data.get('overall_assessment', 'Analysis complete'))
                                    st.info(f"**Role:** {data.get('target_role', target_role)}")
                                
                                # Skills
                                col_s1, col_s2 = st.columns(2)
                                
                                with col_s1:
                                    st.markdown(f"""<div class='card'><h3>✅ Skills You Have ({len(data.get('matching_skills', []))})</h3></div>""", unsafe_allow_html=True)
                                    for skill in data.get('matching_skills', [])[:15]:
                                        st.write(f"• {skill}")
                                
                                with col_s2:
                                    st.markdown(f"""<div class='card'><h3>❌ Skills Job Requires ({len(data.get('mismatching_skills', []))})</h3></div>""", unsafe_allow_html=True)
                                    for skill in data.get('mismatching_skills', [])[:15]:
                                        st.write(f"• {skill}")
                                
                                st.success("✨ Ready to view detailed analysis! Check other tabs.")
                            else:
                                st.error(f"❌ Analysis failed: {response.text}")
                        except Exception as e:
                            st.error(f"❌ Error: {str(e)}")
    
    # ==================== TAB 3: RESUME SCORE ====================
    with tabs[2]:
        st.markdown("""
        <div class='card'>
            <h2>⭐ Resume Score Dashboard</h2>
            <p>Comprehensive analysis of your resume performance</p>
        </div>
        """, unsafe_allow_html=True)
        
        if not st.session_state.role_matching_done:
            st.warning("⚠️ **Please complete Role Matching analysis first (Tab 2)**")
        else:
            if st.button("📊 Calculate Score", use_container_width=True, type="primary"):
                with st.spinner("🔄 Calculating ATS score..."):
                    try:
                        headers = get_auth_headers()
                        payload = {
                            "resume_id": st.session_state.resume_id,
                            "job_description": st.session_state.job_description
                        }
                        
                        response = requests.post(
                            f"{API_BASE_URL}/resume/resume-score",
                            json=payload,
                            headers=headers
                        )
                        
                        if response.status_code == 200:
                            data = response.json()
                            st.session_state.analysis_results['resume_score'] = data
                            
                            # Overall score
                            col_overall = st.columns(1)[0]
                            ats_score = data.get('ats_score', 0)
                            
                            fig_main = go.Figure(data=[
                                go.Indicator(
                                    mode="gauge+number",
                                    value=ats_score,
                                    title={"text": "Overall ATS Score"},
                                    gauge={
                                        "axis": {"range": [0, 100]},
                                        "bar": {"color": "#23b5d3"},
                                        "steps": [
                                            {"range": [0, 30], "color": "#fecaca"},
                                            {"range": [30, 60], "color": "#fcd34d"},
                                            {"range": [60, 100], "color": "#86efac"}
                                        ]
                                    }
                                )
                            ])
                            fig_main.update_layout(height=350)
                            st.plotly_chart(fig_main, use_container_width=True)
                            
                            # Category breakdown
                            st.markdown("### 📊 Category Breakdown")
                            
                            breakdown = data.get("score_breakdown", {})
                            col_cat1, col_cat2, col_cat3, col_cat4 = st.columns(4)
                            
                            categories_list = [
                                ("Technical Skills", breakdown.get("technical_skills", 0), "#23b5d3"),
                                ("Experience", breakdown.get("experience", 0), "#62929e"),
                                ("Education", breakdown.get("education", 0), "#ef8354"),
                                ("Achievements", breakdown.get("achievements", 0), "#23b5d3")
                            ]
                            
                            for col, (name, score, color) in zip([col_cat1, col_cat2, col_cat3, col_cat4], categories_list):
                                with col:
                                    fig = go.Figure(data=[
                                        go.Indicator(
                                            mode="gauge+number",
                                            value=score,
                                            title={"text": name},
                                            gauge={
                                                "axis": {"range": [0, 100]},
                                                "bar": {"color": color}
                                            }
                                        )
                                    ])
                                    fig.update_layout(height=250)
                                    st.plotly_chart(fig, use_container_width=True)
                            
                            # Strengths and Weaknesses
                            col_sw1, col_sw2 = st.columns(2)
                            
                            with col_sw1:
                                st.markdown("### 💪 Strengths")
                                for strength in data.get("strengths", []):
                                    st.success(f"✅ {strength}")
                            
                            with col_sw2:
                                st.markdown("### 🎯 Areas to Improve")
                                for weakness in data.get("weaknesses", []):
                                    st.warning(f"⚠️ {weakness}")
                            
                            # ATS Keywords
                            with st.expander("🔑 ATS Keywords Found"):
                                keywords = data.get("ats_keywords_found", [])
                                if keywords:
                                    for kw in keywords:
                                        st.write(f"• {kw}")
                            
                            # Suggestions
                            with st.expander("💡 Improvement Suggestions"):
                                suggestions = data.get("improvement_suggestions", [])
                                for i, suggestion in enumerate(suggestions, 1):
                                    st.write(f"{i}. {suggestion}")
                        else:
                            st.error(f"❌ Error: {response.text}")
                    except Exception as e:
                        st.error(f"❌ Error: {str(e)}")
    
    # ==================== TAB 4: SKILL GAP ====================
    with tabs[3]:
        st.markdown("""
        <div class='card'>
            <h2>🔍 Skill Gap Analysis</h2>
            <p>Detailed breakdown of your skills vs job requirements</p>
        </div>
        """, unsafe_allow_html=True)
        
        if not st.session_state.role_matching_done:
            st.warning("⚠️ **Please complete Role Matching analysis first (Tab 2)**")
        else:
            if st.button("🔎 Analyze Gaps", use_container_width=True, type="primary"):
                with st.spinner("🔄 Analyzing skill gaps..."):
                    try:
                        headers = get_auth_headers()
                        payload = {
                            "resume_id": st.session_state.resume_id,
                            "job_description": st.session_state.job_description,
                            "target_role": st.session_state.target_role
                        }
                        
                        response = requests.post(
                            f"{API_BASE_URL}/resume/skill-gap",
                            json=payload,
                            headers=headers
                        )
                        
                        if response.status_code == 200:
                            data = response.json()
                            st.session_state.analysis_results['skill_gap'] = data
                            
                            # Summary metrics
                            col_m1, col_m2, col_m3 = st.columns(3)
                            with col_m1:
                                st.metric("Current Skills", len(data.get("current_skills", [])))
                            with col_m2:
                                st.metric("Required Skills", len(data.get("required_skills", [])))
                            with col_m3:
                                gap_pct = data.get('gap_percentage', 0)
                                st.metric("Gap %", f"{gap_pct}%")
                            
                            # Gap visualization
                            fig_gap = go.Figure(data=[
                                go.Pie(
                                    labels=['Covered', 'Gap'],
                                    values=[100 - gap_pct, gap_pct],
                                    marker=dict(colors=['#23b5d3', '#ef8354']),
                                    hole=0.3
                                )
                            ])
                            fig_gap.update_layout(height=350)
                            st.plotly_chart(fig_gap, use_container_width=True)
                            
                            # Skills comparison
                            col_s1, col_s2 = st.columns(2)
                            
                            with col_s1:
                                st.markdown("### ✅ Your Current Skills")
                                current_skills = data.get('current_skills', [])
                                for skill in current_skills:
                                    st.write(f"• {skill}")
                            
                            with col_s2:
                                st.markdown("### ❌ Missing Skills (Priority)")
                                missing_skills = data.get('missing_skills', [])
                                for skill in missing_skills:
                                    st.write(f"• {skill}")
                            
                            # Priority roadmap
                            with st.expander("🎯 Priority Skills to Learn"):
                                for i, skill in enumerate(data.get('priority_missing_skills', []), 1):
                                    st.write(f"**{i}. {skill}**")
                        else:
                            st.error(f"❌ Error: {response.text}")
                    except Exception as e:
                        st.error(f"❌ Error: {str(e)}")
    
    # ==================== TAB 5: UPSKILLING ====================
    with tabs[4]:
        st.markdown("""
        <div class='card'>
            <h2>📚 Upskilling Recommendations</h2>
            <p>Personalized learning paths to bridge your skill gaps</p>
        </div>
        """, unsafe_allow_html=True)
        
        if not st.session_state.role_matching_done:
            st.warning("⚠️ **Please complete Role Matching analysis first (Tab 2)**")
        else:
            col_u1, col_u2 = st.columns(2)
            
            with col_u1:
                hours_per_week = st.slider(
                    "Available Hours per Week",
                    min_value=1,
                    max_value=40,
                    value=10,
                    step=1
                )
            
            with col_u2:
                st.info(f"With **{hours_per_week} hours/week**, you can upskill efficiently!")
            
            if st.button("📖 Generate Learning Paths", use_container_width=True, type="primary"):
                with st.spinner("🔄 Generating personalized learning paths..."):
                    try:
                        headers = get_auth_headers()
                        
                        # Get missing skills from skill gap
                        if 'skill_gap' not in st.session_state.analysis_results:
                            st.warning("First analyzing skill gaps...")
                            payload_gap = {
                                "resume_id": st.session_state.resume_id,
                                "job_description": st.session_state.job_description,
                                "target_role": st.session_state.target_role
                            }
                            response_gap = requests.post(
                                f"{API_BASE_URL}/resume/skill-gap",
                                json=payload_gap,
                                headers=headers
                            )
                            if response_gap.status_code == 200:
                                st.session_state.analysis_results['skill_gap'] = response_gap.json()
                        
                        missing_skills = st.session_state.analysis_results.get('skill_gap', {}).get('priority_missing_skills', [])
                        
                        payload = {
                            "resume_id": st.session_state.resume_id,
                            "missing_skills": missing_skills,
                            "available_hours_per_week": hours_per_week
                        }
                        
                        response = requests.post(
                            f"{API_BASE_URL}/resume/upskilling-recommendations",
                            json=payload,
                            headers=headers
                        )
                        
                        if response.status_code == 200:
                            data = response.json()
                            st.session_state.analysis_results['upskilling'] = data
                            
                            # Summary
                            col_sum1, col_sum2 = st.columns(2)
                            with col_sum1:
                                st.metric("Total Skills", data.get('total_recommendations', 0))
                            with col_sum2:
                                st.metric("Estimated Time", f"{data.get('estimated_total_weeks', 0)} weeks")
                            
                            # Recommendations
                            recommendations = data.get('upskilling_recommendations', [])
                            if recommendations:
                                for i, rec in enumerate(recommendations, 1):
                                    with st.expander(f"📚 {i}. {rec.get('skill', 'Skill')} - {rec.get('estimated_time_weeks', '?')} weeks"):
                                        col_r1, col_r2 = st.columns(2)
                                        
                                        with col_r1:
                                            st.write(f"**Priority:** {rec.get('priority', 'N/A').upper()}")
                                            st.write(f"**Duration:** {rec.get('estimated_time_weeks', '?')} weeks")
                                        
                                        with col_r2:
                                            st.write(f"**Learning Path Steps:**")
                                            for step in rec.get('learning_path_steps', [])[:5]:
                                                st.write(f"→ {step}")
                                        
                                        if rec.get('learning_resources'):
                                            st.markdown("**📖 Recommended Resources:**")
                                            for res in rec.get('learning_resources', [])[:3]:
                                                res_title = res.get('title', 'Resource') if isinstance(res, dict) else res
                                                st.markdown(f"- **{res_title}**")
                            
                            # Priority roadmap
                            with st.expander("🗺️ Priority Learning Roadmap"):
                                for i, item in enumerate(data.get('priority_roadmap', []), 1):
                                    st.write(f"{i}. {item}")
                        else:
                            st.error(f"❌ Error: {response.text}")
                    except Exception as e:
                        st.error(f"❌ Error: {str(e)}")
    
    # ==================== TAB 6: INTERVIEW PREP ====================
    with tabs[5]:
        st.markdown("""
        <div class='card'>
            <h2>🎤 Interview Preparation</h2>
            <p>Custom interview questions based on your profile and target role</p>
        </div>
        """, unsafe_allow_html=True)
        
        if not st.session_state.role_matching_done:
            st.warning("⚠️ **Please complete Role Matching analysis first (Tab 2)**")
        else:
            num_questions = st.slider(
                "Number of Interview Questions",
                min_value=3,
                max_value=10,
                value=5
            )
            
            if st.button("🎤 Generate Interview Questions", use_container_width=True, type="primary"):
                with st.spinner("🔄 Generating interview questions..."):
                    try:
                        headers = get_auth_headers()
                        payload = {
                            "resume_id": st.session_state.resume_id,
                            "job_description": st.session_state.job_description,
                            "target_role": st.session_state.target_role,
                            "num_questions": num_questions
                        }
                        
                        response = requests.post(
                            f"{API_BASE_URL}/resume/interview-questions",
                            json=payload,
                            headers=headers
                        )
                        
                        if response.status_code == 200:
                            data = response.json()
                            st.session_state.analysis_results['interview_prep'] = data
                            
                            st.success(f"✅ Generated {num_questions} Interview Questions!")
                            
                            # Questions
                            for i, q in enumerate(data.get('interview_questions', []), 1):
                                with st.expander(f"❓ **Q{i}: {q.get('question', '')[:60]}...**"):
                                    col_q1, col_q2 = st.columns(2)
                                    
                                    with col_q1:
                                        st.write(f"**Type:** {q.get('question_type', 'General')}")
                                        st.write(f"**Difficulty:** {q.get('difficulty', 'Medium')}")
                                    
                                    with col_q2:
                                        st.write(f"**Related Skill:** {q.get('related_skill', 'N/A')}")
                                    
                                    st.markdown("**💡 Answer Tips:**")
                                    for tip in q.get('answer_tips', []):
                                        st.write(f"• {tip}")
                                    
                                    if q.get('sample_answer'):
                                        st.markdown("**📝 Sample Answer:**")
                                        st.write(q.get('sample_answer'))
                                    
                                    st.markdown("**✅ Key Points to Cover:**")
                                    for point in q.get('key_points_to_cover', []):
                                        st.write(f"→ {point}")
                            
                            # Preparation tips
                            with st.expander("💡 Interview Preparation Tips"):
                                tips = data.get('preparation_tips', [])
                                for tip in tips:
                                    st.write(f"• {tip}")
                            
                            # Common questions
                            with st.expander(f"❓ Common Questions for {st.session_state.target_role}"):
                                common = data.get('common_questions_for_role', [])
                                for q in common:
                                    st.write(f"• {q}")
                        else:
                            st.error(f"❌ Error: {response.text}")
                    except Exception as e:
                        st.error(f"❌ Error: {str(e)}")

if __name__ == "__main__":
    resume_page()
