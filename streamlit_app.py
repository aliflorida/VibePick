# streamlit_app.py (Enhanced with UI polish, homepage, and email prompt)
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

# --- Welcome Screen ---
st.title("🎉 Welcome to VibePick")
st.markdown("Where groups (or solo adventurers) match their vibe and discover things to do — online or IRL.")

with st.expander("📘 How it works"):
    st.markdown("""
    1. Create or join a group session.
    2. Add your info, vibe, and preferred activities.
    3. Get personalized suggestions based on your inputs!
    4. Share ideas or plan a trip with your group.
    """)

st.divider()

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
        if mode == "Group":
            st.success(f"New group created! Share this Group Session ID: {session_id}")
    st.session_state["mode"] = mode
    st.rerun()

if "session_id" not in st.session_state:
    st.stop()

session_id = st.session_state["session_id"]
mode = st.session_state["mode"]

# --- Participant Info & Preferences ---
st.markdown("### 🧑 Add Your Info")
with st.form("user_info_form"):
    name = st.text_input("Your Name")
    email = st.text_input("Your Email (used only to share results)")
    location = st.text_input("Your Location (City or Region)")
    availability = st.selectbox("When are you available?", ["This weekend", "Next week", "Later today", "Flexible", "I'll enter dates below"])
    dates = st.date_input("Preferred Date(s)", [])
    vibe = st.multiselect("What vibe are you feeling?", ["Relaxing", "Adventurous", "Creative", "Social"])
    event_type = st.selectbox("Preferred Event Type", ["In-person", "Virtual", "Hybrid"])
    activity_keywords = st.multiselect("What kind of activities are you into?", ["Live music", "Workshops", "Food", "Fitness", "Tech", "VR", "Games"])
    email_list = st.text_input("Group Emails (comma-separated, optional)")
    submit_user = st.form_submit_button("Submit & Generate Ideas")

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
        st.success("✅ Your details are saved! Gathering recommendations...")
    except Exception as e:
        st.error(f"❌ Failed to save data. {e}")

    if mode == "Group":
        st.markdown(f"📋 Share this Group Session ID: `{session_id}`")

        try:
            users = get_session_users(session_id)
            st.markdown("### 🧑‍🤝‍🧑 Group Members")
            for u in users:
                st.markdown(f"- **{u['name']}** ({u['location']}) – {u['vibe']}")
        except:
            st.warning("No users found yet.")

    st.markdown("### 🎯 Suggested Ideas")
    if not activity_keywords:
        st.warning("Please choose at least one activity.")
    else:
        try:
            events = search_virtual_events(activity_keywords, location=location)
            if not events:
                st.warning("No matches found.")
            for e in events:
                st.markdown(f"- [{e['name']}]({e['url']}) – {e['date']}")
        except Exception as e:
            st.error(f"Error fetching suggestions: {e}")

    if email_list:
        try:
            email_arr = [e.strip() for e in email_list.split(",") if e.strip()]
            if email:
                email_arr.append(email.strip())
            send_group_email(email_arr, get_session_users(session_id), session_id)
            st.success("📧 Emails sent!")
        except Exception as e:
            st.error(f"Failed to send emails. {e}")

# --- Optional Trip Planning ---
st.subheader("🌍 Group Trip Planner")
with st.form("trip_form"):
    planning = st.checkbox("Planning a trip?")
    destination = st.text_input("Where to?")
    est_dates = st.date_input("Estimated Trip Dates")
    submit_trip = st.form_submit_button("Save Trip Plan")

if submit_trip and planning:
    try:
        save_trip_to_session(session_id, {
            "destination": destination,
            "dates": str(est_dates)
        })
        st.success("🗺 Trip saved!")
    except Exception as e:
        st.error(f"❌ Couldn’t save trip info. {e}")
