
import firebase_admin
from firebase_admin import credentials, db

# Path to your working service account JSON file
SERVICE_ACCOUNT_PATH = "C:/Users/aliso/OneDrive/certificates/kaggle/final/dataset/pathfinder-notebook-import/vibefind/firebase/vibepick-b358b-firebase-adminsdk-fbsvc-e1c875451e.json"
DATABASE_URL = "https://vibepick-b358b-default-rtdb.firebaseio.com/"

# Initialize Firebase using local service account JSON
def init_firebase():
    if not firebase_admin._apps:
        cred = credentials.Certificate(SERVICE_ACCOUNT_PATH)
        firebase_admin.initialize_app(cred, {"databaseURL": DATABASE_URL})

# Save user data to session
def save_user_to_session(session_id, user_data):
    try:
        ref = db.reference(f"sessions/{session_id}/users")
        ref.push(user_data)
    except Exception as e:
        print("Firebase write error (users):", e)

# Save trip info to session
def save_trip_to_session(session_id, trip_data):
    try:
        ref = db.reference(f"sessions/{session_id}/trip")
        ref.set(trip_data)
    except Exception as e:
        print("Firebase write error (trip):", e)

# Retrieve all user entries in session
def get_session_users(session_id):
    try:
        ref = db.reference(f"sessions/{session_id}/users")
        return ref.get() or {}
    except Exception as e:
        print("Firebase user read error:", e)
        return {}

# Retrieve trip data
def get_trip_data(session_id):
    try:
        ref = db.reference(f"sessions/{session_id}/trip")
        return ref.get() or {}
    except Exception as e:
        print("Firebase trip read error:", e)
        return {}
