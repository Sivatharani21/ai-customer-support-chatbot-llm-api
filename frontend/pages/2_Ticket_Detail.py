import streamlit as st
import requests
import os

BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:8000")

st.set_page_config(page_title="Ticket Detail", page_icon="🔍")
st.title("🔍 Ticket Detail")

ticket_id = st.session_state.get("selected_ticket_id")

if not ticket_id:
    st.warning("No ticket selected. Please go back to the Tickets page.")
    if st.button("← Back to Tickets"):
        st.switch_page("pages/1_Tickets.py")
    st.stop()

try:
    res = requests.get(f"{BACKEND_URL}/tickets/{ticket_id}", timeout=10)
    if res.status_code == 404:
        st.error("Ticket not found.")
        st.stop()
    ticket = res.json()
except Exception as e:
    st.error(f"Could not fetch ticket: {e}")
    st.stop()

st.markdown(f"### Ticket `{ticket['ticket_id']}`")
st.divider()

col1, col2 = st.columns(2)
col1.metric("Status", ticket["status"].title())
col2.metric("Intent", ticket["intent"].replace("_", " ").title())

st.markdown("#### Details")
fields = {
    "Session ID": ticket.get("session_id"),
    "Order Number": ticket.get("order_id"),
    "Product": ticket.get("product"),
    "Quantity": ticket.get("quantity"),
    "Invoice Number": ticket.get("invoice_number"),
    "Description": ticket.get("description"),
    "Created At": ticket.get("created_at", "")[:19].replace("T", " "),
}

for label, value in fields.items():
    if value:
        st.markdown(f"**{label}:** {value}")

st.divider()
if st.button("← Back to Tickets"):
    st.switch_page("pages/1_Tickets.py")
