import streamlit as st

st.set_page_config(page_title="AI Leaderboard", layout="wide")

def leaderboard_page():

    # 🔑 Simulated logged-in user
    current_user = "Kanishka"

    # -------------------------
    # Leaderboard Data
    # -------------------------
    users = [
        {"name": "Bhumika", "score": 980, "accuracy": "96%", "quizzes": 120, "img": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQ4Liy_zASrwEOvXDzt-R54FRhPj3li5c3RNA&s"},
        {"name": "Rohit", "score": 940, "accuracy": "93%", "quizzes": 115, "img": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRpD1b0xa3uTTqRUtDQgmlCVWJjZAmUGdv8Kw&s"},
        {"name": "Gauri", "score": 910, "accuracy": "91%", "quizzes": 108, "img": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcR66j3HYpb35UuSTwGcJpbuwcAogHhTD1-hdg&s"},
        {"name": "Dnyaneshwari", "score": 715, "accuracy": "81%", "quizzes": 33, "img": "https://i.pinimg.com/564x/11/35/54/11355485abdadd6a47bcd886ee5e7395.jpg"},
        {"name": "Priyanka", "score": 745, "accuracy": "83%", "quizzes": 35, "img": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRe660q-PUl7JC6968MMHlaWcxRIsyecKSsQA&s"},
        {"name": "Harsh", "score": 870, "accuracy": "89%", "quizzes": 102, "img": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQ6Wqd247vlE2eH6XPS2ctyldo7ZUUK-YlZsg&s"},
        {"name": "Kanishka", "score": 780, "accuracy": "85%", "quizzes": 37, "img": "https://miro.medium.com/v2/resize:fit:1400/1*b_yNY_575wRgAcUq4b9Kpg.jpeg"},
        {"name": "Raj", "score": 850, "accuracy": "88%", "quizzes": 98, "img": "https://www.cuahangmmo.net/assets/storage/images/avatarNGQ.png"},
        {"name": "Rohan", "score": 760, "accuracy": "84%", "quizzes": 36, "img": "https://imptechsol.com/images/face2.jpg"},
        {"name": "Siddharth", "score": 730, "accuracy": "82%", "quizzes": 34, "img": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQY6vjXrihfo1H_aym3QWDwHpz3X4PlHYqC6Q&s"},
        {"name": "Aditya", "score": 700, "accuracy": "80%", "quizzes": 32, "img": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcR4DK-7fAUqQJR_lOZWTnd_9_V0JI0FHRhIyQ&s"},
    ]

    # -------------------------
    # Styles (with hover effects)
    # -------------------------
    st.markdown("""
    <style>
    .top-card {
        background: #1e1e2f;
        border-radius: 20px;
        padding: 22px;
        text-align: center;
        color: white;
        transition: all 0.25s ease;
    }

    .top-card:hover {
        transform: translateY(-6px) scale(1.03);
        box-shadow: 0 18px 40px rgba(0,0,0,0.4);
    }

    .medal {
        font-size: 56px;
    }

    .top-card img {
        width: 80px;
        height: 80px;
        border-radius: 50%;
        border: 4px solid white;
        margin: 10px 0;
    }

    .ribbon {
        display: grid;
        grid-template-columns: 1fr 3fr 2fr 2fr 2fr;
        background: linear-gradient(90deg,#ff7a18,#ffb347);
        padding: 14px;
        border-radius: 14px;
        font-weight: 700;
        margin: 30px 0 10px;
    }

    .row {
        display: grid;
        grid-template-columns: 1fr 3fr 2fr 2fr 2fr;
        padding: 12px;
        border-radius: 12px;
        margin-bottom: 8px;
        background: #f4f4f4;
        align-items: center;
        transition: all 0.2s ease;
    }

    .row:hover {
        transform: scale(1.02);
        background: #ffffff;
        box-shadow: 0 12px 26px rgba(0,0,0,0.15);
    }

    .current-user {
        background: linear-gradient(90deg,#c6ffdd,#fbd786,#f7797d);
        border: 2px solid #ff9800;
        font-weight: 800;
    }

    .user {
        display: flex;
        align-items: center;
        gap: 12px;
    }

    .user img {
        width: 42px;
        height: 42px;
        border-radius: 50%;
    }

    .you-badge {
        background: #ff9800;
        color: white;
        padding: 4px 10px;
        border-radius: 12px;
        font-size: 12px;
        margin-left: 8px;
    }
    </style>
    """, unsafe_allow_html=True)

    # -------------------------
    # Header
    # -------------------------
    st.markdown("""
    <div class="header-main">
        <h1>🏆 AI Leaderboard</h1>
        <p>See How You Rank Among Learners</p>
    </div>
    """, unsafe_allow_html=True)

    # st.selectbox("📊 Leaderboard Type", ["Global", "Monthly", "Weekly"])

    # -------------------------
    # Your Rank
    # -------------------------
    user_rank = next((i for i,u in enumerate(users, start=1) if u["name"] == current_user), None)
    if user_rank:
        st.success(f"🎯 Your current rank: #{user_rank}")

    # -------------------------
    # Top 3
    # -------------------------
    medals = ["🥇", "🥈", "🥉"]
    top3 = users[:3]

    col1, col2, col3 = st.columns(3)
    for col, u, medal in zip([col1, col2, col3], top3, medals):
        with col:
            st.markdown(f"""
            <div class="top-card">
                <div class="medal">{medal}</div>
                <img src="{u['img']}">
                <h3>{u['name']}</h3>
                <div>{u['score']} pts</div>
                <div>Accuracy: {u['accuracy']}</div>
                <div>Quizzes: {u['quizzes']}</div>
            </div>
            """, unsafe_allow_html=True)

    # -------------------------
    # Ribbon Header
    # -------------------------
    st.markdown("""
    <div class="ribbon">
        <div>Rank</div>
        <div>User</div>
        <div>Score</div>
        <div>Accuracy</div>
        <div>Quizzes</div>
    </div>
    """, unsafe_allow_html=True)

    # -------------------------
    # Leaderboard Table
    # -------------------------
    for idx, u in enumerate(users, start=1):

        is_current = u["name"] == current_user
        row_class = "row current-user" if is_current else "row"
        badge = "<span class='you-badge'>YOU</span>" if is_current else ""

        st.markdown(f"""
        <div class="{row_class}">
            <div>#{idx}</div>
            <div class="user">
                <img src="{u['img']}">
                <div>{u['name']} {badge}</div>
            </div>
            <div>{u['score']}</div>
            <div>{u['accuracy']}</div>
            <div>{u['quizzes']}</div>
        </div>
        """, unsafe_allow_html=True)