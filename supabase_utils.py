
# supabase_utils.py
import os
import requests
import json

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_API_KEY = os.getenv("SUPABASE_API_KEY")
MAILERSEND_API_KEY = os.getenv("MAILERSEND_API_KEY")

HEADERS = {
    "apikey": SUPABASE_API_KEY,
    "Authorization": f"Bearer {SUPABASE_API_KEY}",
    "Content-Type": "application/json"
}

def create_session_id():
    import uuid
    return str(uuid.uuid4())

def save_user_to_session(session_id, user_data):
    response = requests.post(
        f"{SUPABASE_URL}/rest/v1/session_users",
        headers=HEADERS,
        data=json.dumps(user_data)
    )
    response.raise_for_status()

def get_session_users(session_id):
    response = requests.get(
        f"{SUPABASE_URL}/rest/v1/session_users?session_id=eq.{session_id}",
        headers=HEADERS
    )
    response.raise_for_status()
    return response.json()

def save_trip_to_session(session_id, trip_data):
    response = requests.post(
        f"{SUPABASE_URL}/rest/v1/trip_plans",
        headers=HEADERS,
        data=json.dumps(trip_data)
    )
    response.raise_for_status()

def get_trip_data(session_id):
    response = requests.get(
        f"{SUPABASE_URL}/rest/v1/trip_plans?id=eq.{session_id}",
        headers=HEADERS
    )
    response.raise_for_status()
    return response.json()

def send_group_email(email_list, users, session_id):
    content = f"Hi from VibePick!\n\nYour group session ({session_id}) includes the following participants:\n\n"
    for u in users:
        content += f"- {u['name']} ({u['location']}) – {u['vibe']}\n"

    payload = {
        "from": {"email": "noreply@vibepick.app", "name": "VibePick"},
        "to": [{"email": e} for e in email_list],
        "subject": "Your VibePick Group Plan",
        "text": content
    }

    response = requests.post(
        "https://api.mailersend.com/v1/email",
        headers={
            "Authorization": f"Bearer {MAILERSEND_API_KEY}",
            "Content-Type": "application/json"
        },
        data=json.dumps(payload)
    )
    response.raise_for_status()
