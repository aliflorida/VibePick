
import firebase_admin
from firebase_admin import credentials, db
import uuid

# Initialize Firebase App (only once)
def init_firebase(api_key, project_id, db_url):
    if not firebase_admin._apps:
        cred = credentials.Certificate({
            "type": "service_account",
            "project_id": project_id,
            "private_key_id": api_key["private_key_id"],
            "private_key": api_key["private_key"].replace("\\n", "\n"),
            "client_email": api_key["client_email"],
            "client_id": api_key["client_id"],
            "auth_uri": "https://accounts.google.com/o/oauth2/auth",
            "token_uri": "https://oauth2.googleapis.com/token",
            "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
            "client_x509_cert_url": api_key["client_x509_cert_url"]
        })
        firebase_admin.initialize_app(cred, {"databaseURL": db_url})

# Store user entry under a session ID
def save_user_to_session(session_id, user_data):
    ref = db.reference(f"sessions/{session_id}/users")
    ref.push(user_data)

# Save trip info
def save_trip_to_session(session_id, trip_data):
    ref = db.reference(f"sessions/{session_id}/trip")
    ref.set(trip_data)

# Retrieve all users in a session
def get_session_users(session_id):
    ref = db.reference(f"sessions/{session_id}/users")
    return ref.get() or {}

# Retrieve trip data
def get_trip_data(session_id):
    ref = db.reference(f"sessions/{session_id}/trip")
    return ref.get() or {}
