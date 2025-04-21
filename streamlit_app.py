
import streamlit as st
from firebase_admin import db

st.title("🔥 Firebase Write Test")

# Direct write test button
if st.button("🔥 Write Directly to Firebase"):
    try:
        test_ref = db.reference("/debug_direct_write")
        test_ref.set({"status": "Hello from Streamlit"})
        st.success("✅ Successfully wrote to Firebase!")
    except Exception as e:
        st.error(f"Firebase error: {e}")
