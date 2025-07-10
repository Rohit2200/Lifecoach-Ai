
import streamlit as st
import requests

st.set_page_config(page_title="LifeCoach AI", page_icon="🧠")

# custom CSS
st.markdown("""
<style>
    .main { background-color: #111111; color: #f0f0f0; }
    div.stButton > button {
        border-radius: 8px;
        background-color: #6366f1;
        color: white;
        font-weight: 600;
        padding: 0.6em 1em;
        border: none;
    }
    .stTextInput > div > input {
        background-color: #1f1f1f;
        color: white;
        border-radius: 6px;
    }
    .stMarkdown {
        color: #ffffff;
    }
</style>
""", unsafe_allow_html=True)

# Page Setup
st.title("🧠 LifeCoach AI")
st.subheader("Personalized Plans for Health, Finance, Learning & Motivation")

# --- User ID ---
user_id = st.text_input("🔐 Enter your name or ID to start:", key="user_id_input")
if not user_id:
    st.warning("Please enter your ID to proceed.")
    st.stop()

# --- Load Chat History ---
if "chat_history" not in st.session_state:
    try:
        res = requests.get(f"http://localhost:8000/chat-history/{user_id}")
        st.session_state.chat_history = res.json() if res.status_code == 200 else []
    except:
        st.session_state.chat_history = []

# --- Load Saved Plans ---
try:
    plans_res = requests.get(f"http://localhost:8000/load-plan-names/{user_id}")
    saved_plans = plans_res.json().get("plans", []) if plans_res.status_code == 200 else []
except:
    saved_plans = []

# --- Plan Generator ---
with st.expander("📋 Generate a Custom Life Plan", expanded=True):
    with st.form("plan_form"):
        plan_name = st.text_input("📌 Name this Plan", placeholder="e.g., Week1_BulkPlan")
        goal = st.text_input("🎯 Health Goal", placeholder="e.g., Build muscles and eat more protein")
        income = st.text_input("💸 Monthly Income (in ₹)", placeholder="e.g., 100000")
        learning_goal = st.text_input("📚 Learning Goal", placeholder="e.g., Learn data science with Python")
        duration = st.slider("📆 Duration (Days)", min_value=1, max_value=7, value=1)
        submitted = st.form_submit_button("🧠 Generate My Plan")

    if submitted:
        with st.spinner("Generating plan..."):
            try:
                response = requests.post(
                    f"http://localhost:8000/life-plan?save_name={plan_name}&user_id={user_id}&v2=true",
                    json={
                        "goal": goal,
                        "income": income,
                        "learning_goal": learning_goal,
                        "duration": duration
                    }
                )
                if response.status_code == 200:
                    plan = response.json()["plan"]
                    st.success(f"✅ Plan '{plan_name}' generated!")

                    if isinstance(plan, dict):
                        for key, emoji in {
                            "health_plan": "🧠",
                            "learning_plan": "📚",
                            "motivation_plan": "🌟",
                            "finance_plan": "💰"
                        }.items():
                            with st.expander(f"{emoji} {key.replace('_', ' ').title()}"):
                                st.markdown(plan.get(key, "❌ Missing"))
                    else:
                        st.markdown("### 📋 Full Life Plan")
                        st.markdown(plan)
                else:
                    st.error("❌ Failed to generate plan.")
            except:
                st.error("❌ Backend not reachable.")

# --- Load/Edit/Delete Plans ---
with st.expander("♻️ Load, Edit or Delete a Saved Plan"):
    if saved_plans:
        selected_plan = st.selectbox("📁 Choose a saved plan:", saved_plans)
        col1, col2, col3 = st.columns(3)

        with col1:
            if st.button("🔁 Load"):
                try:
                    res = requests.get(f"http://localhost:8000/load-plan/{user_id}/{selected_plan}")
                    if res.status_code == 200:
                        plan = res.json()["plan"]
                        st.session_state.loaded_plan = plan
                        st.session_state.plan_display_name = selected_plan
                        st.success("✅ Plan Loaded.")
                    else:
                        st.error("❌ Plan not found.")
                except:
                    st.error("❌ Could not connect to backend.")

        with col2:
            if st.button("🗑️ Delete"):
                try:
                    res = requests.delete(f"http://localhost:8000/delete-plan/{user_id}/{selected_plan}")
                    if res.status_code == 200:
                        st.success("✅ Plan deleted.")
                        st.rerun()
                    else:
                        st.error("❌ Failed to delete.")
                except:
                    st.error("❌ Could not connect to backend.")

        with col3:
            if st.button("✏️ Edit"):
                try:
                    res = requests.get(f"http://localhost:8000/load-plan/{user_id}/{selected_plan}")
                    if res.status_code == 200:
                        st.session_state.edit_mode = True
                        st.session_state.plan_to_edit = selected_plan
                        st.session_state.plan_data = res.json()["plan"]
                        st.rerun()
                except:
                    st.error("❌ Could not load for editing.")
    else:
        st.info("No saved plans found.")

# --- Edit Mode ---
if st.session_state.get("edit_mode", False):
    st.markdown(f"## 📝 Editing Plan: `{st.session_state.plan_to_edit}`")
    plan_data = st.session_state.plan_data

    if isinstance(plan_data, str):
        st.text_area("📋 Full Plan (read-only)", plan_data, height=400)
    else:
        edited = {}
        for key, label in {
            "health_plan": "🧠 Health Plan",
            "learning_plan": "📚 Learning Plan",
            "motivation_plan": "🌟 Motivation Tips",
            "finance_plan": "💰 Finance Plan"
        }.items():
            edited[key] = st.text_area(label, plan_data.get(key, ""))

        if st.button("💾 Save Changes"):
            try:
                res = requests.put(
                    f"http://localhost:8000/update-plan/{user_id}/{st.session_state.plan_to_edit}",
                    json=edited
                )
                if res.status_code == 200:
                    st.success("✅ Plan updated!")
                    st.session_state.edit_mode = False
                    st.rerun()
                else:
                    st.error("❌ Failed to update.")
            except:
                st.error("❌ Could not connect to backend.")

# --- Agent Chat ---
with st.expander("💬 Talk to a Life Coach Agent"):
    agent_choice = st.selectbox("Choose Agent", ["Health", "Finance", "Learning", "Motivation"])
    user_message = st.text_input("Type your message")

    if st.button("Ask Agent"):
        if user_message.strip():
            try:
                res = requests.post("http://localhost:8000/agent-chat", json={
                    "user_id": user_id,
                    "agent": agent_choice.lower(),
                    "message": user_message
                })
                if res.status_code == 200:
                    reply = res.json()["response"]
                    st.session_state.chat_history.append({
                        "user": user_message,
                        "agent": reply,
                        "type": agent_choice
                    })
                    st.success(f"{agent_choice} Coach replied:")
                    st.markdown(f"🧍‍♂️ You: `{user_message}`\n\n🤖 {agent_choice}: {reply}")
                else:
                    st.error("❌ Agent failed.")
            except:
                st.error("❌ Could not connect.")
        else:
            st.warning("Enter a question first.")

# --- Display Chat History ---
if st.session_state.get("chat_history"):
    with st.expander("🧾 Chat History"):
        for chat in reversed(st.session_state.chat_history):
            st.markdown(f"🧍‍♂️ **You ({chat['type']}):** {chat['user']}")
            st.markdown(f"🤖 **{chat['type']} Coach:** {chat['agent']}")
            st.markdown("---")

# --- Clear Chat ---
if st.button("🗑️ Clear Chat History"):
    try:
        res = requests.delete(f"http://localhost:8000/clear-chat/{user_id}")
        if res.status_code == 200:
            st.session_state.chat_history = []
            st.success("✅ Chat history cleared.")
        else:
            st.error("❌ Failed to clear.")
    except:
        st.error("❌ Could not connect to backend.")
