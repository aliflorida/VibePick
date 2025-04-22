
# streamlit_app.py
import streamlit as st
from supabase_utils import (
    create_session_id,
    save_user_to_session,
    get_session_users,
    save_trip_to_session,
    get_trip_data,
    send_group_email
)
from virtual_event_utils import search_virtual_events
import uuid
import os

st.set_page_config(page_title="VibePick", layout="centered")

st.title("🎉 VibePick – Find Your Group Vibe")

# --- Session Setup ---
st.markdown("### 👥 Join or Start a Group")

with st.form("session_join_form"):
    mode = st.radio("Are you planning solo or with a group?", ["Group", "Solo"])
    session_id_input = st.text_input("Enter your Group Session ID (or leave blank to create one):")
    submitted = st.form_submit_button("Continue")

if submitted:
    if session_id_input.strip():
        session_id = session_id_input.strip()
        st.session_state["session_id"] = session_id
    else:
        session_id = create_session_id()
        st.session_state["session_id"] = session_id
        st.success(f"New group created! Share this Group Session ID: {session_id}")

    st.rerun()

if "session_id" not in st.session_state:
    st.stop()

session_id = st.session_state["session_id"]

# --- Participant Info & Preferences ---
if mode == "Group":
    st.markdown("### 🧑 Add Your Info")
    with st.form("user_info_form"):
        name = st.text_input("Your Name")
        location = st.text_input("Your Location")
        availability = st.selectbox("When are you available?", ["This weekend", "Next week", "Later today", "Flexible"])
        dates = st.date_input("Select your preferred date(s)", [])
        vibe = st.multiselect("What vibe are you feeling?", ["Relaxing", "Adventurous", "Creative", "Social"])
        event_type = st.selectbox("Preferred Event Type", ["In-person", "Virtual", "Hybrid"])
        activity_keywords = st.multiselect("Preferred Activities", ["Live music", "Workshops", "Food", "Fitness", "Tech", "VR", "Games"])
        email_list = st.text_input("Optional: Enter group emails to share results (comma-separated)")
        submit_user = st.form_submit_button("Submit and Generate")

    if submit_user and name and location:
        user_data = {
            "id": str(uuid.uuid4()),
            "session_id": session_id,
            "name": name,
            "location": location,
            "available": availability,
            "vibe": ",".join(vibe),
        }
        try:
            save_user_to_session(session_id, user_data)
            st.success("✅ Group details saved! Gathering recommendations...")
        except Exception as e:
            st.error(f"❌ Failed to save group data. {e}")

        st.markdown(f"📋 Share this Group Session ID: `{session_id}`")

        try:
            users = get_session_users(session_id)
            st.markdown("### 🧑‍🤝‍🧑 Group Members")
            for u in users:
                st.markdown(f"- **{u['name']}** ({u['location']}) – {u['vibe']}")
        except Exception as e:
            st.warning("No users found in session.")
            st.text(f"Debug: {e}")

        st.markdown("### 🎯 Suggested Ideas")

        if not activity_keywords:
            st.warning("Please select at least one activity to get suggestions.")
        else:
            try:
                events = search_virtual_events(activity_keywords, location=location)
                if not events:
                    st.warning("No suggestions found for your preferences.")
                for e in events:
                    st.markdown(f"- [{e['name']}]({e['url']}) – {e['date']}")
            except Exception as e:
                st.error(f"⚠️ Failed to fetch suggestions: {e}")

        if email_list:
            try:
                email_arr = [e.strip() for e in email_list.split(",")]
                send_group_email(email_arr, users, session_id)
                st.success("📧 Email sent to your group!")
            except Exception as e:
                st.error(f"⚠️ Failed to send group email. Error: {e}")

# --- Trip Planning ---
st.subheader("🌍 Optional: Group Trip Planning")
with st.form("trip_form"):
    planning = st.checkbox("Are you planning a trip together?")
    destination = st.text_input("Destination (city or region)")
    est_dates = st.text_input("Estimated trip dates")
    submit_trip = st.form_submit_button("Save Trip Info")

if submit_trip and planning:
    try:
        save_trip_to_session(session_id, {
            "id": session_id,
            "session_id": session_id,
            "destination": destination,
            "dates": est_dates
        })
        st.success("🗺 Trip saved!")
    except Exception as e:
        st.error(f"❌ Trip save failed. {e}")
