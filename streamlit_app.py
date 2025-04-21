import streamlit as st
import openai
import uuid
from supabase_utils import (
    save_user_to_session,
    save_trip_to_session,
    get_session_users,
    get_trip_data
)

st.set_page_config(page_title="VibePick", layout="wide")

st.title("🎯 VibePick: Group Decision Maker")

# --- SESSION SETUP ---
if "session_id" not in st.session_state:
    st.session_state.session_id = str(uuid.uuid4())

session_id = st.session_state.session_id
st.markdown(f"🆔 Session ID: `{session_id}`")

# --- USER INFO ---
with st.form("user_form"):
    st.subheader("🙋 Your Info")
    name = st.text_input("Name")
    location = st.text_input("Where are you located?")
    available = st.text_input("When are you free?")
    vibe = st.multiselect("What type of vibe are you feeling?", ["Chill", "Adventurous", "Foodie", "Cultural", "Virtual"])
    submitted = st.form_submit_button("Join Session")

    if submitted and name:
        user_data = {
            "name": name,
            "location": location,
            "available": available,
            "vibe": vibe
        }
        save_user_to_session(session_id, user_data)
        st.success("✅ You’ve been added to the session!")

# --- GROUP SUMMARY ---
st.subheader("👥 Group Vibe Check")
users = get_session_users(session_id)

if users:
    for user in users:
        st.markdown(f"- **{user.get('name', 'Unnamed')}** from _{user.get('location', 'Unknown')}_ wants a **{', '.join(user.get('vibe', []))}** vibe.")
else:
    st.info("No one has joined this session yet.")

# --- TRIP PLANNING ---
st.subheader("🌍 Optional: Group Trip Planning")
with st.form("trip_form"):
    planning = st.checkbox("Are you planning a trip together?")
    destination = st.text_input("Destination (city or region)")
    est_dates = st.text_input("Estimated trip dates")
    trip_submit = st.form_submit_button("Add Trip Info")

    if trip_submit and planning and destination:
        trip_data = {
            "planning": planning,
            "destination": destination,
            "dates": est_dates
        }
        save_trip_to_session(session_id, trip_data)
        st.success("🧳 Trip details saved!")

trip = get_trip_data(session_id)
if trip:
    st.info(f"🗺️ Planning a trip to **{trip['destination']}** around _{trip['dates']}_")

# --- Footer ---
st.markdown("---")
st.caption("Built with ❤️ for collaborative planners. VibePick 2025.")