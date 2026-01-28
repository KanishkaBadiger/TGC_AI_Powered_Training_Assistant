import streamlit as st
import requests
import time
import plotly.graph_objects as go

API_BASE_URL = "http://127.0.0.1:8000/api"
QUESTION_TIME = 30  # seconds per question


def quiz_page():
    # ---------------- TITLE CARD ----------------
    st.markdown("""
    <div class='header-main'>
        <h1>📝 AI Quiz Generator</h1>
        <p>Your Brain's New Workout Partner</p>
    </div>
    """, unsafe_allow_html=True)

    # ---------------- SESSION STATE INITIALIZATION ----------------
    # We initialize user_id here just in case it wasn't set by login
    # This prevents the "AttributeError" crash
    if "user_id" not in st.session_state:
        st.session_state.user_id = 1  # Default ID for safety

    st.session_state.setdefault("quiz", None)
    st.session_state.setdefault("answers", {})
    st.session_state.setdefault("results", None)
    st.session_state.setdefault("current_q", 0)
    st.session_state.setdefault("quiz_started", False)
    st.session_state.setdefault("start_time", None)
    st.session_state.setdefault("celebrated", False)

    # ---------------- QUIZ SETTINGS ----------------
    if not st.session_state.quiz_started and not st.session_state.results:
        st.subheader("⚙️ Quiz Settings")

        domain = st.selectbox(
            "Domain",
            ["Data Science", "AI", "ML", "Web Development", "Cyber Security"]
        )

        category = st.selectbox(
            "Category",
            ["Aptitude", "Technical", "Coding"]
        )

        difficulty = st.select_slider(
            "Difficulty",
            ["Easy", "Medium", "Hard"]
        )

        num_questions = st.slider("Number of Questions", 1, 20, 5)

        if st.button("🚀 Generate Quiz"):
            # Prepare payload exactly as your backend expects it
            payload = {
                "user_id": st.session_state.user_id,
                "domain": domain,
                "category": category,
                "difficulty": difficulty,
                "num_questions": num_questions
            }

            try:
                with st.spinner("🤖 AI is curating your quiz..."):
                    response = requests.post(
                        f"{API_BASE_URL}/quiz/generate",
                        json=payload,
                        timeout=25
                    )

                    if response.status_code == 200:
                        st.session_state.quiz = response.json()
                        st.session_state.quiz_started = True
                        st.session_state.current_q = 0
                        st.session_state.answers = {}
                        st.session_state.start_time = time.time()
                        st.session_state.celebrated = False
                        st.rerun()
                    else:
                        st.error(f"❌ Failed to generate quiz: {response.text}")

            except Exception as e:
                st.error(f"❌ Connection error: {e}")

    # ---------------- QUIZ FLOW ----------------
    if st.session_state.quiz_started and st.session_state.quiz:
        q_idx = st.session_state.current_q
        
        # Safety check for index
        if q_idx < len(st.session_state.quiz):
            question = st.session_state.quiz[q_idx]

            elapsed = int(time.time() - st.session_state.start_time)
            remaining = max(0, QUESTION_TIME - elapsed)

            st.markdown(f"⏱ **Time Left:** `{remaining}` seconds")

            st.markdown(f"### Q{q_idx + 1}. {question['question']}")

            selected = st.radio(
                "Choose your answer:",
                question["options"],
                index=None,
                key=f"q_{question['id']}"
            )

            if selected:
                st.session_state.answers[question["id"]] = selected

            col1, col2 = st.columns(2)

            with col1:
                if st.button("✅ Submit"):
                    move_next_question()
                    st.rerun()

            with col2:
                if st.button("⏭ Skip"):
                    move_next_question()
                    st.rerun()

            if remaining == 0:
                move_next_question()
                st.rerun()

    # ---------------- RESULTS ----------------
    if st.session_state.results:
        st.subheader("📊 Quiz Performance Summary")

        # Handle list vs dict response format safely
        results_data = st.session_state.results
        if isinstance(results_data, dict) and "results" in results_data:
             results_data = results_data["results"]
        
        if not results_data:
             st.warning("No results available.")
             return

        total = len(results_data)
        correct = sum(1 for r in results_data if r.get("is_correct", False))
        
        # Calculate wrong and unattempted
        wrong = 0
        unattempted = 0
        for r in results_data:
             if r.get("is_correct", False):
                 continue
             if r.get("your_answer") is None:
                 unattempted += 1
             else:
                 wrong += 1

        score_percent = int((correct / total) * 100) if total > 0 else 0

        st.markdown(
            f"""
            <div style="text-align:center;">
                <h2>🎯 Score: {correct}/{total}</h2>
                <h3 style="color:#0066cc;">{score_percent}% Accuracy</h3>
            </div>
            """,
            unsafe_allow_html=True
        )

        # -------- DYNAMIC DONUT PIE --------
        fig = go.Figure(
            data=[
                go.Pie(
                    labels=["Correct", "Wrong", "Unattempted"],
                    values=[correct, wrong, unattempted],
                    hole=0.45,
                    textinfo="label+percent",
                    hoverinfo="label+value+percent",
                    pull=[0.06, 0.04, 0],
                    marker=dict(
                        colors=["#2ECC71", "#E74C3C", "#F1C40F"],
                        line=dict(color="white", width=2)
                    ),
                )
            ]
        )

        fig.update_layout(
            title=dict(text="📈 Answer Distribution", x=0.5),
            transition=dict(duration=800),
            margin=dict(t=80, b=40)
        )

        st.plotly_chart(fig, use_container_width=True)

        # -------- BADGE SYSTEM --------
        if score_percent >= 90:
            badge = "🏆 QUIZ MASTER"
        elif score_percent >= 75:
            badge = "🥇 EXCELLENT"
        elif score_percent >= 50:
            badge = "🥈 GOOD ATTEMPT"
        else:
            badge = "🥉 KEEP PRACTICING"

        st.markdown(
            f"""
            <div style="
                background:#f0f8ff;
                padding:30px;
                border-radius:20px;
                text-align:center;
                box-shadow:0 6px 15px rgba(0,0,0,0.15);
            ">
                <h1 style="font-size:60px;">{badge}</h1>
                <p style="font-size:18px;">Keep improving 🚀</p>
            </div>
            """,
            unsafe_allow_html=True
        )

        if not st.session_state.celebrated:
            st.balloons()
            st.session_state.celebrated = True

        st.divider()

        st.subheader("📝 Detailed Review")

        for i, r in enumerate(results_data):
            q_text = r.get('question_text', f"Question {i+1}")
            user_ans = r.get('your_answer', 'Skipped')
            correct_ans = r.get('correct_answer', 'N/A')
            explanation = r.get('explanation', 'No explanation provided.')
            is_correct = r.get('is_correct', False)

            with st.expander(f"Q{i+1}: {q_text}"):
                 if is_correct:
                     st.success(f"✅ Your Answer: {user_ans}")
                 else:
                     st.error(f"❌ Your Answer: {user_ans}")
                     st.markdown(f"**Correct Answer:** `{correct_ans}`")
                 
                 st.info(f"💡 {explanation}")

        if st.button("🔄 Start New Quiz"):
             st.session_state.results = None
             st.session_state.quiz_started = False
             st.session_state.quiz = None
             st.rerun()


# ---------------- HELPER ----------------
def move_next_question():
    if st.session_state.current_q + 1 < len(st.session_state.quiz):
        st.session_state.current_q += 1
        st.session_state.start_time = time.time()
    else:
        # Final submission
        payload = {
            "user_id": st.session_state.user_id,
            "answers": st.session_state.answers
        }

        try:
            response = requests.post(
                f"{API_BASE_URL}/quiz/submit",
                json=payload
            )

            if response.status_code == 200:
                st.session_state.results = response.json()
                st.session_state.quiz_started = False
            else:
                st.error("Failed to submit quiz results.")
        except Exception as e:
            st.error(f"Submission Error: {e}")