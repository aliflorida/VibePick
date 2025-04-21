import firebase_admin
from firebase_admin import credentials, db
import streamlit as st
import json

def init_firebase():
    if not firebase_admin._apps:
        cred = credentials.Certificate(dict(st.secrets["FIREBASE_CREDENTIALS"]))
        firebase_admin.initialize_app(cred, {
            "databaseURL": st.secrets["FIREBASE_DB_URL"]
        })

def save_user_to_session(session_id, user_data):
    try:
        ref = db.reference(f"sessions/{session_id}/users")
        ref.push(user_data)
    except Exception as e:
        print("Firebase write error (users):", e)

def save_trip_to_session(session_id, trip_data):
    try:
        ref = db.reference(f"sessions/{session_id}/trip")
        ref.set(trip_data)
    except Exception as e:
        print("Firebase write error (trip):", e)

def get_session_users(session_id):
    try:
        ref = db.reference(f"sessions/{session_id}/users")
        return ref.get() or {}
    except Exception as e:
        print("Firebase user read error:", e)
        return {}

def get_trip_data(session_id):
    try:
        ref = db.reference(f"sessions/{session_id}/trip")
        return ref.get() or {}
    except Exception as e:
        print("Firebase trip read error:", e)
        return {}