# frontend/pages/Roadmap.py
import streamlit as st
import requests
from datetime import date, datetime, timedelta
from streamlit_calendar import calendar
import json

st.set_page_config(page_title="AI Personalized Roadmap", layout="wide")


API_URL = "http://localhost:8000/api/roadmap"


def roadmap_page():

    # Try to get the user from session state
    current_user = st.session_state.get('user', None)

    if current_user:
        # ✅ User is logged in, use their real ID
        USER_ID = current_user['id']
    else:
        # ⚠️ User NOT logged in (e.g., Page Refresh or Direct Access)
        # OPTION A: For Dev/Testing, fallback to "1" so it doesn't crash
        # USER_ID = "1" 
        
        # OPTION B: Safer Production Approach
        # Just stop silently or show a sidebar note, but don't block aggressively.
        st.sidebar.error("⚠️ Session expired. Please re-login to save progress.")
        USER_ID = None # We will handle this 'None' gracefully below

    # --- CUSTOM CSS STYLING ---
    st.markdown("""
    <div class='header-main'>
        <h1>🛣️ Personalized Learning Roadmap</h1>
        <p>Your Path to Career Goals</p>
    </div>


    <style>
        /* 1. Main Background */
        .stApp { background-color: #f4f6f9; color: #212529; }
        
        /* 2. Card Styling */
        .css-card {
            background-color: #ffffff;
            border: 1px solid #e1e4e8;
            border-radius: 12px;
            padding: 24px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.04);
            margin-bottom: 20px;
        }
                
        /* 3. CALENDAR STYLING */
        .fc-theme-standard {
            background-color: #ffffff;
            border-radius: 12px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.08);
            padding: 15px;
            border: 1px solid #e1e4e8;
        }
        .fc-toolbar-title { font-size: 1.4rem !important; color: #2c3e50; font-weight: 700; }
        .fc-col-header-cell { background-color: #f8f9fa; color: #6c757d; padding: 10px 0; border-bottom: 2px solid #e9ecef; }
        .fc-day-today { background-color: #fff8e1 !important; }

        /* Event Styling */
        .fc-event {
            border-radius: 6px; 
            padding: 4px 8px; 
            font-size: 0.8rem; 
            border: none; 
            box-shadow: 0 2px 4px rgba(0,0,0,0.1); 
            margin-bottom: 4px;
            font-weight: 600;
            cursor: pointer;
            transition: transform 0.2s ease;
        }
        .fc-event:hover { transform: scale(1.03); z-index: 100 !important; }
        
        /* 4. Resource Links */
        .resource-link {
            display: block;
            padding: 12px 16px;
            margin: 8px 0;
            background-color: #f8f9fa;
            border-left: 4px solid #0d6efd;
            border-radius: 4px;
            text-decoration: none;
            color: #2c3e50 !important;
            font-weight: 600;
            transition: all 0.2s ease;
        }
        .resource-link:hover { background-color: #e9ecef; transform: translateX(5px); }
        
        /* Warning Box Styling */
        .stAlert { padding: 1rem; border-radius: 10px; }
                
        /* 🎯 TARGET THE SUBMIT BUTTON SPECIFICALLY */
        div[data-testid="stFormSubmitButton"] > button {
            background: linear-gradient(135deg, #ef8354 0%, #e07040 100%) !important;
            color: white !important;
            border: 1px solid #ef8354 !important;
            font-weight: bold !important;
        }

        /* HOVER STATE */
        div[data-testid="stFormSubmitButton"] > button:hover {
            background-color: #e36a0e !important;
            border-color: #e36a0e !important;
            color: white !important;
            box-shadow: 0 8px 20px rgba(239, 131, 84, 0.3) !important
            transform: scale(1.02);
        }

        /* CLICKED/ACTIVE STATE */
        div[data-testid="stFormSubmitButton"] > button:active,
        div[data-testid="stFormSubmitButton"] > button:focus {
            background-color: #d05e0b !important;
            border-color: #d05e0b !important;
            color: white !important;
            box-shadow: none !important;
        }
    </style>
    """, unsafe_allow_html=True)

    # --- STATE MANAGEMENT ---
    if 'selected_event' not in st.session_state:
        st.session_state.selected_event = None
    if 'confirm_reset' not in st.session_state:
        st.session_state.confirm_reset = False
    if 'show_onboarding' not in st.session_state:
        st.session_state.show_onboarding = False

    # --- FETCH DATA ---
    def get_dashboard_data():
        if not USER_ID: return None # Safety exit
        
        # If user wants to start fresh, don't fetch data
        if st.session_state.get("show_onboarding", False):
            return None
            
        try:
            res = requests.get(f"{API_URL}/dashboard/{USER_ID}")
            if res.status_code == 200:
                return res.json()
        except:
            pass
        return None

    data = get_dashboard_data()

    # ==========================================
    # 🚀 1. ONBOARDING (Start New)
    # ==========================================
    if not data or data.get("status") == "no_roadmap":
        st.title("🛣️ Create Your Personal Roadmap 🚀")
        st.info("Start your journey by defining your goal below.")
        
        with st.form("new_roadmap_form"):
            col1, col2 = st.columns(2)
            with col1:
                role = st.selectbox("I want to become a...", ["Frontend Developer", "Backend Developer", "Full Stack Dev", "Data Scientist", "SDE (DSA Focus)", "DevOps Engineer", "Machine Learning Engineer", "Data Engineer"])
                level = st.selectbox("Current Level", ["Beginner", "Intermediate", "Advanced"])
            
            with col2:
                r_type = st.radio("Focus Area", ["DSA (Algorithms)", "Development (Projects)", "Mixed (Best for Jobs)"])
                target_date = st.date_input("Target Date", min_value=date.today(), value=date.today() + timedelta(days=30))

            submitted = st.form_submit_button("🚀 Generate AI Roadmap")
            
            if submitted:
                with st.spinner("🤖 AI is crafting your new schedule..."):
                    payload = {
                        "user_id": USER_ID,
                        "role": role,
                        "skill_level": level,
                        "roadmap_type": r_type,
                        "end_date": str(target_date)
                    }
                    try:
                        res = requests.post(f"{API_URL}/generate", params=payload)
                        if res.status_code == 200:
                            st.success("New Roadmap Created!")
                            st.session_state.show_onboarding = False 
                            st.session_state.confirm_reset = False
                            st.rerun()
                        else:
                            st.error(f"Error: {res.text}")
                    except Exception as e:
                        st.error(f"Connection Failed: {e}")
        st.stop() # Stop here

    # ==========================================
    # 📊 2. DASHBOARD
    # ==========================================
    roadmap = data['roadmap_details']
    tasks = data.get('all_tasks', [])

    # --- HEADER & CONTROLS ---
    col1, col2, col3, col4 = st.columns([3, 1, 1, 1])

    with col1:
        st.title(f"🚀 {roadmap['role']} Mastery")
        st.markdown(f"**Level:** {roadmap['skill_level']} &nbsp;|&nbsp; **Focus:** Tech & DSA")

    with col2:
        # PAUSE BUTTON
        is_paused = roadmap['is_paused']
        if st.button("▶️ RESUME" if is_paused else "⏸ PAUSE", key="pause_btn", use_container_width=True):
            requests.post(f"{API_URL}/toggle_pause/{roadmap['id']}")
            st.rerun()

    with col3:
        # REFRESH BUTTON
        if st.button("🔄 Refresh", use_container_width=True):
            st.rerun()

    with col4:
        # START NEW BUTTON (Triggers Warning)
        if st.button("🆕 Start a New Roadmap", use_container_width=True):
            st.session_state.confirm_reset = True
            st.rerun()

    # --- WARNING BOX (Conditional Render) ---
    if st.session_state.confirm_reset:
        with st.container():
            st.markdown("---")
            st.warning("⚠️ **Are you sure you want to end your current roadmap journey?**")
            st.markdown("This action cannot be undone. You will lose the current progress record for this specific goal.")
            
            b_col1, b_col2, b_col3 = st.columns([1, 1, 4])
            with b_col1:
                if st.button("✅ Yes, Start New", type="primary", use_container_width=True):
                    st.session_state.show_onboarding = True # Force onboarding view
                    st.session_state.confirm_reset = False # Hide warning
                    st.session_state.selected_event = None # Clear selection
                    st.rerun()
            with b_col2:
                if st.button("❌ Cancel", use_container_width=True):
                    st.session_state.confirm_reset = False # Hide warning
                    st.rerun()
            st.markdown("---")

    # --- MAIN CALENDAR & DETAILS ---
    st.markdown("<br>", unsafe_allow_html=True)
    left_col, right_col = st.columns([2.5, 1.2])

    # --- LEFT: CALENDAR ---
    with left_col:
        events = []
        today_str = str(date.today())

        for task in tasks:
            # Tag Logic
            bg_color = "#6c757d"
            title_prefix = "⏳ UPCOMING"
            
            if task['status'] == "COMPLETED": 
                bg_color = "#198754"
                title_prefix = "✅ COMPLETED"
            elif task['status'] == "MISSED": 
                bg_color = "#dc3545"
                title_prefix = "⚠️ PENDING"
            elif task['status'] == "PENDING" and task['date_assigned'] == today_str: 
                bg_color = "#fd7e14"
                title_prefix = "🔄 ONGOING"
            elif task['status'] == "PAUSED":
                bg_color = "#ffc107"
                title_prefix = "⏸ PAUSED"

            events.append({
                "title": f"{title_prefix}: {task['module_name']}",
                "start": task['date_assigned'],
                "backgroundColor": bg_color,
                "borderColor": bg_color,
                "textColor": "#ffffff",
                "extendedProps": {
                    "topic": task['topic'],
                    "desc": task['description'],
                    "resources": task['resources'],
                    "status": task['status'],
                    "display_status": title_prefix,
                    "id": task['id']
                }
            })

        calendar_options = {
            "initialView": "dayGridMonth",
            "headerToolbar": {"left": "prev,next today", "center": "title", "right": ""},
            "height": 750,
            "contentHeight": "auto",
            "fixedWeekCount": False,
            "showNonCurrentDates": False,
        }

        st.subheader("📅 Your Schedule")
        cal_state = calendar(events=events, options=calendar_options, key="roadmap_cal")

        if cal_state.get("eventClick"):
            st.session_state.selected_event = cal_state["eventClick"]["event"]

    # --- RIGHT: DETAILS PANEL ---
    with right_col:
        selected = st.session_state.selected_event
        st.markdown('<div class="css-card">', unsafe_allow_html=True)
        
        if not selected:
            # TODAY'S DEFAULT
            current_task = next((t for t in tasks if t['date_assigned'] == today_str), None)
            
            if current_task:
                status_text = "✅ COMPLETED" if current_task['status'] == "COMPLETED" else "🔄 ONGOING"
                status_color = "#198754" if current_task['status'] == "COMPLETED" else "#fd7e14"

                st.markdown(f"### 📅 Today's Focus")
                st.markdown(f"<span style='background-color: {status_color}; color: white; padding: 4px 10px; border-radius: 12px; font-size: 0.8em; font-weight: bold;'>{status_text}</span>", unsafe_allow_html=True)
                st.markdown(f"**Topic:** {current_task['topic']}")
                st.info(f"💡 {current_task['description']}")
                
                st.markdown("#### 📚 Study Resources")
                if current_task['resources']:
                    try:
                        res_list = current_task['resources'] if isinstance(current_task['resources'], list) else json.loads(current_task['resources'])
                        for r in res_list:
                            st.markdown(f'<a href="{r["url"]}" target="_blank" class="resource-link">🔗 {r["title"]}</a>', unsafe_allow_html=True)
                    except:
                        st.warning("Could not load resources.")
                
                st.markdown("---")
                if current_task['status'] != "COMPLETED":
                    if st.button("✅ Mark as Completed", type="primary", use_container_width=True):
                        requests.post(f"{API_URL}/complete/{current_task['id']}")
                        st.balloons()
                        st.rerun()
            else:
                st.success("🎉 You are caught up!")
                st.markdown("Click any date on the calendar to see details.")

        else:
            # SELECTED EVENT
            props = selected["extendedProps"]
            badge_color = selected['backgroundColor']
            badge_text = props['display_status']
            
            st.markdown(f"### 📌 {props['topic']}")
            st.markdown(f"<span style='background-color: {badge_color}; color: white; padding: 5px 12px; border-radius: 15px; font-weight: bold; font-size: 0.9em;'>{badge_text}</span>", unsafe_allow_html=True)
            st.markdown(f"<div style='margin-top:15px; color:#555;'>{props['desc']}</div>", unsafe_allow_html=True)
            
            st.markdown("#### 📚 Resources")
            if props['resources']:
                try:
                    res_list = props['resources'] if isinstance(props['resources'], list) else json.loads(props['resources'])
                    for r in res_list:
                        st.markdown(f'<a href="{r["url"]}" target="_blank" class="resource-link">🔗 {r["title"]}</a>', unsafe_allow_html=True)
                except:
                    st.warning("No resources found.")
            
            st.markdown("---")
            if props['status'] != "COMPLETED":
                if st.button("Mark as Done", key="mark_done_selected", type="primary", use_container_width=True):
                    requests.post(f"{API_URL}/complete/{props['id']}")
                    st.session_state.selected_event = None
                    st.balloons()
                    st.rerun()
            else:
                st.markdown("✅ *Task Completed!*")

        st.markdown('</div>', unsafe_allow_html=True)