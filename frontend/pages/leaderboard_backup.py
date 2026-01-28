# import streamlit as st
# import pandas as pd

# def leaderboard_page():
#     """Leaderboard Page"""
#     st.markdown("""
#     <div class='header-main'>
#         <h1>🏆 Leaderboards & Achievements</h1>
#         <p>See How You Rank Among Learners</p>
#     </div>
#     """, unsafe_allow_html=True)
    
#     lb_type = st.selectbox("📊 Leaderboard Type", ["Global", "Category", "Weekly"])
    
#     st.markdown("---")
    
#     leaderboard_data = {
#         "Rank": [1, 2, 3, 4, 5],
#         "User": ["Alice Chen", "Bob Kumar", "Charlie Brown", "Diana Prince", "Your Name"],
#         "Points": [4850, 4620, 4390, 4210, 3950],
#         "Quizzes": [156, 148, 142, 135, 128],
#         "Accuracy": ["94%", "91%", "88%", "85%", "78%"]
#     }
    
#     df = pd.DataFrame(leaderboard_data)
#     st.dataframe(df, use_container_width=True, hide_index=True)
    
#     st.markdown("---")
    
#     col_l1, col_l2, col_l3, col_l4 = st.columns(4)
#     with col_l1:
#         st.metric("Your Rank", "#5")
#     with col_l2:
#         st.metric("Points", "3950")
#     with col_l3:
#         st.metric("Streak", "12 days")
#     with col_l4:
#         st.metric("Accuracy", "78%")



import streamlit as st
import requests
import pandas as pd
import time

st.set_page_config(page_title="Community Leaderboard", page_icon="🏆", layout="wide")

# --- AUTH CHECK ---
USER = st.session_state.get('user', {"id": None, "username": "Guest"})
API_URL = "http://localhost:8000/api/gamify"

def leaderboard_page():
    """Leaderboard Page"""
    st.markdown("""
    <div class='header-main'>
        <h1>🏆 Leaderboards & Achievements</h1>
        <p>See How You Rank Among Learners</p>
    </div>
    """, unsafe_allow_html=True)


    # --- CUSTOM CSS FOR PODIUM & CARDS ---
    st.markdown("""
    <style>
        /* Main Background */
        .stApp { background-color: #f8f9fa; color: #212529; }
        
        /* Card Styling */
        .css-card {
            background-color: #ffffff;
            border: 1px solid #e1e4e8;
            border-radius: 12px;
            padding: 20px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.04);
            margin-bottom: 20px;
            text-align: center;
        }
        
        /* Stats Numbers */
        .stat-number { font-size: 28px; font-weight: 800; color: #fd7e14; }
        .stat-label { font-size: 14px; color: #6c757d; text-transform: uppercase; letter-spacing: 1px; }
        
        /* Podium Colors */
        .rank-1 { border-top: 5px solid #FFD700; } /* Gold */
        .rank-2 { border-top: 5px solid #C0C0C0; } /* Silver */
        .rank-3 { border-top: 5px solid #CD7F32; } /* Bronze */
        
        /* User Row in Table */
        .user-row {
            background: white; padding: 15px; border-radius: 8px;
            margin-bottom: 8px; border: 1px solid #eee;
            display: flex; justify-content: space-between; align-items: center;
        }
    </style>
    """, unsafe_allow_html=True)

    st.title("🏆 Community Leaderboard")
    st.markdown("Competition drives consistency. See where you stand!")

    # --- FETCH DATA ---
    try:
        res = requests.get(f"{API_URL}/leaderboard")
        if res.status_code == 200:
            leaderboard = res.json()
        else:
            leaderboard = []
    except:
        st.error("⚠️ Connection Error. Ensure Backend is running.")
        st.stop()

    # --- 1. MY STATS SECTION ---
    if USER['id']:
        # Find my data
        my_data = next((item for item in leaderboard if item["username"] == USER['username']), None)
        
        my_rank = leaderboard.index(my_data) + 1 if my_data else "-"
        my_xp = my_data['xp'] if my_data else 0
        my_streak = my_data['streak'] if my_data else 0
        
        st.markdown("### 👤 Your Performance")
        c1, c2, c3 = st.columns(3)
        with c1:
            st.markdown(f'<div class="css-card"><div class="stat-number">#{my_rank}</div><div class="stat-label">Current Rank</div></div>', unsafe_allow_html=True)
        with c2:
            st.markdown(f'<div class="css-card"><div class="stat-number">{my_xp} XP</div><div class="stat-label">Total Experience</div></div>', unsafe_allow_html=True)
        with c3:
            st.markdown(f'<div class="css-card"><div class="stat-number">🔥 {my_streak}</div><div class="stat-label">Day Streak</div></div>', unsafe_allow_html=True)

    # --- 2. TOP 3 PODIUM ---
    if len(leaderboard) >= 3:
        st.markdown("### 🌟 Top Performers")
        col1, col2, col3 = st.columns([1, 1, 1])
        
        # 🥈 Silver (2nd)
        with col1:
            p2 = leaderboard[1]
            st.markdown(f"""
            <div class="css-card rank-2" style="margin-top: 20px;">
                <h3>🥈 2nd Place</h3>
                <h4 style="color:#555;">{p2['username']}</h4>
                <div class="stat-number">{p2['xp']} XP</div>
                <small>🔥 {p2['streak']} Day Streak</small>
            </div>
            """, unsafe_allow_html=True)
        
        # 🥇 Gold (1st - Center & Highlighted)
        with col2:
            p1 = leaderboard[0]
            st.markdown(f"""
            <div class="css-card rank-1">
                <h1>👑 1st Place</h1>
                <h3 style="color:#212529;">{p1['username']}</h3>
                <div class="stat-number" style="font-size:36px;">{p1['xp']} XP</div>
                <small style="color:#fd7e14; font-weight:bold;">🔥 {p1['streak']} Day Streak</small>
            </div>
            """, unsafe_allow_html=True)
            
        # 🥉 Bronze (3rd)
        with col3:
            p3 = leaderboard[2]
            st.markdown(f"""
            <div class="css-card rank-3" style="margin-top: 20px;">
                <h3>🥉 3rd Place</h3>
                <h4 style="color:#555;">{p3['username']}</h4>
                <div class="stat-number">{p3['xp']} XP</div>
                <small>🔥 {p3['streak']} Day Streak</small>
            </div>
            """, unsafe_allow_html=True)

    # --- 3. FULL RANKING LIST ---
    st.markdown("### 📉 The Chase")

    if leaderboard:
        # Convert to DataFrame for a clean table view
        df = pd.DataFrame(leaderboard)
        df.index += 1 # Rank starts at 1
        df = df.rename(columns={"username": "Student Name", "xp": "Total XP", "streak": "🔥 Consistency Streak"})
        
        # Use Streamlit's new column config for a polished look
        st.dataframe(
            df,
            use_container_width=True,
            column_config={
                "Total XP": st.column_config.ProgressColumn(
                    "XP Progress",
                    format="%d XP",
                    min_value=0,
                    max_value=max(df["Total XP"]) if not df.empty else 100,
                ),
                "🔥 Consistency Streak": st.column_config.NumberColumn(
                    "Streak (Days)",
                    format="%d Days"
                )
            }
        )
    else:
        st.info("No data yet. Be the first to take a quiz!")