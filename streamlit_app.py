
import streamlit as st
from firebase_admin import db
from firebase_utils import init_firebase

# Initialize Firebase correctly before using db
init_firebase(
    st.secrets["FIREBASE_CREDENTIALS"],
    st.secrets["FIREBASE_PROJECT_ID"],
    st.secrets["FIREBASE_DB_URL"]
)

st.title("🔥 Firebase Write Test")

# Direct write test button
if st.button("🔥 Write Directly to Firebase"):
    try:
        test_ref = db.reference("/debug_direct_write")
        test_ref.set({"status": "Hello from Streamlit"})
        st.success("✅ Successfully wrote to Firebase!")
    except Exception as e:
        st.error(f"Firebase error: {e}")
