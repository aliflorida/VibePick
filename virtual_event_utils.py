
import os
import uuid
import requests
from dotenv import load_dotenv

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_SERVICE_KEY")

HEADERS = {
    "apikey": SUPABASE_KEY,
    "Authorization": f"Bearer {SUPABASE_KEY}",
    "Content-Type": "application/json",
}

def create_session_id():
    return str(uuid.uuid4())

def save_user_to_session(session_id, user_data):
    response = requests.post(
        f"{SUPABASE_URL}/rest/v1/session_users",
        headers=HEADERS,
        json=user_data,
    )
    response.raise_for_status()

def get_session_users(session_id):
    response = requests.get(
        f"{SUPABASE_URL}/rest/v1/session_users?session_id=eq.{session_id}",
        headers=HEADERS,
    )
    response.raise_for_status()
    return response.json()

def save_trip_to_session(session_id, trip_data):
    trip_payload = {
        "id": str(uuid.uuid4()),
        "session_id": session_id,
        "destination": trip_data.get("destination", ""),
        "dates": trip_data.get("dates", "")
    }
    response = requests.post(
        f"{SUPABASE_URL}/rest/v1/trip_plans",
        headers=HEADERS,
        json=trip_payload,
    )
    response.raise_for_status()

def get_trip_data(session_id):
    response = requests.get(
        f"{SUPABASE_URL}/rest/v1/trip_plans?session_id=eq.{session_id}",
        headers=HEADERS,
    )
    response.raise_for_status()
    return response.json()

def send_group_email(recipients, users, session_id):
    import smtplib
    from email.mime.text import MIMEText

    body = f"Group Session ID: {session_id}\n\nMembers:\n"
    for u in users:
        body += f"- {u['name']} from {u['location']} — {u['vibe']}\n"

    msg = MIMEText(body)
    msg['Subject'] = 'Your VibePick Group Info'
    msg['From'] = 'noreply@vibepick.app'
    msg['To'] = ', '.join(recipients)

    try:
        with smtplib.SMTP('smtp.mailersend.net', 587) as server:
            server.starttls()
            server.login(os.getenv("MAILERSEND_EMAIL"), os.getenv("MAILERSEND_API_KEY"))
            server.sendmail(msg['From'], recipients, msg.as_string())
    except Exception as e:
        raise RuntimeError(f"Email sending failed: {e}")
