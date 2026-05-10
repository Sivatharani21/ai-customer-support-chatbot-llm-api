import streamlit as st
import requests
import uuid
import os

BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:8000")

st.set_page_config(page_title="B2B Support Chatbot", page_icon="🤖")
st.title("🤖 B2B Customer Support Chatbot")

if "session_id" not in st.session_state:
    st.session_state.session_id = str(uuid.uuid4())

if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

if prompt := st.chat_input("Describe your support issue..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Processing..."):
            try:
                res = requests.post(
                    f"{BACKEND_URL}/chat",
                    json={"message": prompt, "session_id": st.session_state.session_id},
                    timeout=30,
                )
                data = res.json()
                reply = data.get("response", "Sorry, something went wrong.")
                if data.get("ticket_id"):
                    reply += f"\n\n📋 **Ticket ID:** `{data['ticket_id']}`"
            except Exception as e:
                reply = f"⚠️ Could not reach the backend: {e}"

        st.markdown(reply)
        st.session_state.messages.append({"role": "assistant", "content": reply})

with st.sidebar:
    st.subheader("Session Info")
    st.code(st.session_state.session_id, language="text")

    st.divider()
    st.subheader("Past Sessions")
    try:
        sessions_res = requests.get(f"{BACKEND_URL}/sessions", timeout=10)
        sessions = sessions_res.json()
    except:
        sessions = []

    if sessions:
        session_options = {f"{s['session_id'][:8]}... ({s['last_active']})": s['session_id'] for s in sessions}
        selected_label = st.selectbox("Pick a session", list(session_options.keys()))
        selected_session_id = session_options[selected_label]

        if st.button("▶ Continue Session"):
            try:
                res = requests.get(
                    f"{BACKEND_URL}/history",
                    params={"session_id": selected_session_id},
                    timeout=10,
                )
                logs = res.json().get("logs", [])
                st.session_state.session_id = selected_session_id
                st.session_state.messages = []
                for log in logs:
                    st.session_state.messages.append({"role": "user", "content": log["query"]})
                    st.session_state.messages.append({"role": "assistant", "content": log["response"]})
                st.rerun()
            except Exception as e:
                st.error(f"Could not load session: {e}")
    else:
        st.caption("No past sessions found.")

    st.divider()
    if st.button("📋 View All Tickets"):
        st.switch_page("pages/1_Tickets.py")
    if st.button("View Conversation History"):
        try:
            res = requests.get(
                f"{BACKEND_URL}/history",
                params={"session_id": st.session_state.session_id},
                timeout=10,
            )
            history = res.json().get("logs", [])
            for log in history:
                st.markdown(f"**You:** {log['query']}")
                st.markdown(f"**Bot:** {log['response']}")
                st.divider()
        except Exception as e:
            st.error(f"Could not fetch history: {e}")
    if st.button("New Session"):
        st.session_state.session_id = str(uuid.uuid4())
        st.session_state.messages = []
        st.rerun()
