import streamlit as st
import uuid
from supabase_utils import save_user_to_session, save_trip_to_session, get_session_users, get_trip_data
import requests
import os

st.set_page_config(page_title="VibePick", layout="wide")

# Supabase API keys from environment or secrets
SUPABASE_URL = st.secrets.get("SUPABASE_URL", "")
SUPABASE_API_KEY = st.secrets.get("SUPABASE_API_KEY", "")

st.title("🎯 VibePick – Plan Something Fun Together or Solo")

# Mode Selection
mode = st.radio("Who's planning?", ["👤 Just Me", "🧑‍🤝‍🧑 Group Planner"], horizontal=True)

# Generate a unique session ID for this user/session
session_id = str(uuid.uuid4())

# Basic Info
with st.form("vibe_form"):
    name = st.text_input("Your name")
    location = st.text_input("Where are you located?")
    available = st.selectbox("When are you available?", ["Now", "Later today", "This weekend", "Next week"])
    
    vibe = st.multiselect("What’s your vibe?", ["Chill", "Adventurous", "Creative", "Social", "Relaxing", "Productive"])
    activities = st.multiselect("What types of activities are you interested in?", 
        ["Breakfast", "Lunch", "Brunch", "Dinner", "Coffee", "Shopping", "Outdoor", "Entertainment", "Wellness", "Co-working"])
    format_pref = st.multiselect("Preferred event format", ["In-person", "Virtual", "Hybrid"])

    if mode == "🧑‍🤝‍🧑 Group Planner":
        planning = st.checkbox("This is a future plan (we're not together yet)", value=True)

    destination = st.text_input("If you're thinking of a place or vibe, type it here (optional)")
    dates = st.date_input("Date(s) you're considering", [])

    email_results = st.checkbox("Email me the results")
    email_address = st.text_input("Enter your email", "") if email_results else ""

    submitted = st.form_submit_button("🔍 Suggest Ideas")

# Handle submission
if submitted:
    user_data = {
        "name": name,
        "location": location,
        "available": available,
        "vibe": vibe
    }

    if mode == "🧑‍🤝‍🧑 Group Planner":
        save_user_to_session(session_id, user_data)
        save_trip_to_session(session_id, {
            "planning": planning,
            "destination": destination,
            "dates": str(dates)
        })
        st.success("✅ Group details saved! Gathering recommendations...")

        # List group members
        users = get_session_users(session_id)
        st.subheader("🧑‍🤝‍🧑 Group Members")
        for u in users:
            st.markdown(f"- {u['name']} ({u['location']}) - {', '.join(u['vibe'])}")

    else:
        st.success("✅ Solo plan started! Gathering ideas just for you...")

    st.subheader("🎯 Suggested Ideas (Mockup)")
    st.markdown("Here would be live API suggestions based on your filters...")

    if email_results and email_address:
        try:
            requests.post(
                "https://api.mailersend.com/v1/email",
                headers={
                    "Authorization": f"Bearer {st.secrets['MAILERSEND_API_KEY']}",
                    "Content-Type": "application/json"
                },
                json={
                    "from": {"email": "hello@vibepick.app", "name": "VibePick"},
                    "to": [{"email": email_address}],
                    "subject": "Your VibePick Suggestions",
                    "text": "Here's what we think you'll enjoy! (actual results to be inserted here)"
                }
            )
            st.success("📩 Results emailed!")
        except Exception as e:
            st.error(f"Email failed: {e}")