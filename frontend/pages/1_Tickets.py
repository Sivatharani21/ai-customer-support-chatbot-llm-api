import streamlit as st
import requests
import os

BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:8000")

st.set_page_config(page_title="All Tickets", page_icon="📋")
st.title("📋 Support Tickets")

try:
    res = requests.get(f"{BACKEND_URL}/tickets", timeout=10)
    tickets = res.json()
except Exception as e:
    st.error(f"Could not fetch tickets: {e}")
    tickets = []

if not tickets:
    st.info("No tickets found.")
elif not isinstance(tickets, list) or not isinstance(tickets[0], dict):
    st.error(f"Unexpected response format: {tickets}")
else:
    for ticket in tickets:
        col1, col2, col3, col4 = st.columns([2, 2, 2, 1])
        col1.write(f"**{ticket['ticket_id']}**")
        col2.write(ticket["intent"].replace("_", " ").title())
        col3.write(ticket["created_at"][:10])
        status_color = "🟢" if ticket["status"] == "open" else "🔴"
        col4.write(f"{status_color} {ticket['status'].title()}")

        if st.button("View Details", key=ticket["ticket_id"]):
            st.session_state["selected_ticket_id"] = ticket["ticket_id"]
            st.switch_page("pages/2_Ticket_Detail.py")

        st.divider()
