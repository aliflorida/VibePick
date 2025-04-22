import os
import requests
import uuid
import streamlit as st

SUPABASE_URL = os.getenv("SUPABASE_URL", st.secrets.get("SUPABASE_URL", ""))
SUPABASE_API_KEY = os.getenv("SUPABASE_API_KEY", st.secrets.get("SUPABASE_API_KEY", ""))
SUPABASE_HEADERS = {
    "apikey": SUPABASE_API_KEY,
    "Authorization": f"Bearer {SUPABASE_API_KEY}",
    "Content-Type": "application/json"
}

def save_user_to_session(session_id, user_data):
    payload = {
        "id": str(uuid.uuid4()),
        "session_id": session_id,
        "name": user_data.get("name", ""),
        "location": user_data.get("location", ""),
        "available": user_data.get("available", ""),
        "vibe": ",".join(user_data.get("vibe", []))
    }

    st.text("📤 Sending payload to Supabase (session_users):")
    st.json(payload)

    response = requests.post(f"{SUPABASE_URL}/rest/v1/session_users", headers=SUPABASE_HEADERS, json=payload)

    if response.status_code >= 400:
        st.error("❌ Supabase insert failed")
        st.text(f"🔢 Status: {response.status_code}")
        st.text(f"📦 Response: {response.text}")
        response.raise_for_status()

def save_trip_to_session(session_id, trip_data):
    payload = {
        "id": session_id,
        "planning": trip_data.get("planning"),
        "destination": trip_data.get("destination"),
        "dates": trip_data.get("dates")
    }
    headers = SUPABASE_HEADERS.copy()
    headers["Prefer"] = "resolution=merge-duplicates"
    response = requests.post(f"{SUPABASE_URL}/rest/v1/trip_plans", headers=headers, json=payload)
    response.raise_for_status()

def get_session_users(session_id):
    url = f"{SUPABASE_URL}/rest/v1/session_users?session_id=eq.{session_id}"
    response = requests.get(url, headers=SUPABASE_HEADERS)
    response.raise_for_status()
    users = response.json()
    return [{
        "name": u.get("name", ""),
        "location": u.get("location", ""),
        "available": u.get("available", ""),
        "vibe": u.get("vibe", "").split(",") if u.get("vibe") else []
    } for u in users]

def get_trip_data(session_id):
    url = f"{SUPABASE_URL}/rest/v1/trip_plans?id=eq.{session_id}"
    response = requests.get(url, headers=SUPABASE_HEADERS)
    response.raise_for_status()
    trip = response.json()
    return trip[0] if trip else {}