import streamlit as st
import pandas as pd

def leaderboard_page():
    """Leaderboard Page"""
    st.markdown("""
    <div class='header-main'>
        <h1>🏆 Leaderboards & Achievements</h1>
        <p>See How You Rank Among Learners</p>
    </div>
    """, unsafe_allow_html=True)
    
    lb_type = st.selectbox("📊 Leaderboard Type", ["Global", "Category", "Weekly"])
    
    st.markdown("---")
    
    leaderboard_data = {
        "Rank": [1, 2, 3, 4, 5],
        "User": ["Alice Chen", "Bob Kumar", "Charlie Brown", "Diana Prince", "Your Name"],
        "Points": [4850, 4620, 4390, 4210, 3950],
        "Quizzes": [156, 148, 142, 135, 128],
        "Accuracy": ["94%", "91%", "88%", "85%", "78%"]
    }
    
    df = pd.DataFrame(leaderboard_data)
    st.dataframe(df, use_container_width=True, hide_index=True)
    
    st.markdown("---")
    
    col_l1, col_l2, col_l3, col_l4 = st.columns(4)
    with col_l1:
        st.metric("Your Rank", "#5")
    with col_l2:
        st.metric("Points", "3950")
    with col_l3:
        st.metric("Streak", "12 days")
    with col_l4:
        st.metric("Accuracy", "78%")
