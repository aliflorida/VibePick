
import streamlit as st
from firebase_utils import (
    init_firebase,
    save_user_to_session,
    save_trip_to_session,
    get_session_users,
    get_trip_data
)

# Initialize Firebase
init_firebase()

st.title("🔥 VibePick Firebase Test App")

# Session ID (for demonstration purposes, you can replace with uuid or input)
session_id = "demo-session"

# User Input Form
with st.form("user_form"):
    name = st.text_input("Your name")
    email = st.text_input("Your email")
    city = st.text_input("City")
    preferences = st.multiselect("What do you feel like doing?", ["🎬 Movie Night", "🍝 Dinner", "🎮 Game", "🎤 Karaoke"])
    submit = st.form_submit_button("Save User")

if submit and name and email:
    user_data = {
        "name": name,
        "email": email,
        "city": city,
        "preferences": preferences
    }
    save_user_to_session(session_id, user_data)
    st.success("✅ User saved to Firebase!")

# Display existing users in this session
if st.button("Show all users in session"):
    users = get_session_users(session_id)
    if users:
        for uid, info in users.items():
            st.write(f"- {info.get('name')} ({info.get('city')}) — Preferences: {', '.join(info.get('preferences', []))}")
    else:
        st.info("No users found in this session.")

# Optional Trip Planner
with st.expander("Plan a group trip"):
    with st.form("trip_form"):
        destination = st.text_input("Destination")
        date = st.date_input("Trip date")
        submit_trip = st.form_submit_button("Save Trip")
        if submit_trip and destination:
            trip_data = {
                "destination": destination,
                "date": str(date)
            }
            save_trip_to_session(session_id, trip_data)
            st.success("🧳 Trip details saved!")

# Display trip data
if st.button("Show trip details"):
    trip = get_trip_data(session_id)
    if trip:
        st.write(f"📍 Destination: {trip.get('destination')}")
        st.write(f"📅 Date: {trip.get('date')}")
    else:
        st.info("No trip planned yet.")
