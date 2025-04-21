
import streamlit as st
from openai import OpenAI
import uuid
from datetime import date
from place_search_utils import search_foursquare_places
from trip_cost_utils import search_trip_costs
from send_email_utils import send_email
from data_export import save_session_to_csv

# App Config
st.set_page_config(page_title="VibePick", layout="centered")
st.title("🎉 VibePick")
st.caption("Decide together. Pick your vibe.")

# Load secrets
OPENAI_API_KEY = st.secrets["OPENAI_API_KEY"]
FOURSQUARE_API_KEY = st.secrets["FOURSQUARE_API_KEY"]
EVENTBRITE_TOKEN = st.secrets["EVENTBRITE_TOKEN"]
SERPAPI_KEY = st.secrets["SERPAPI_KEY"]
MAILERSEND_API_KEY = st.secrets["MAILERSEND_API_KEY"]
client = OpenAI(api_key=OPENAI_API_KEY)

# Session ID
if "session_id" not in st.session_state:
    st.session_state["session_id"] = str(uuid.uuid4())

# Step 1: Group Info
st.header("Step 1: Group Info")
user_name = st.text_input("Your name:")
user_email = st.text_input("Your email:")
user_city = st.text_input("Your city/location:")
plan_type = st.radio("What type of plan are you making?", ["In-person", "Virtual", "Hybrid"])
future_plan = st.radio("Is this plan for now or in the future?", ["Now", "Future"])
if future_plan == "Future":
    trip_dates = st.date_input("When will you all be together?", [])
else:
    trip_dates = [date.today()]

# Step 2: Group Vibe
st.header("Step 2: Group Vibe")

meal_vibes = [
    "🍳 Breakfast",
    "🥪 Lunch",
    "🍝 Dinner",
    "🥂 Brunch",
    "🍕 Late-Night Eats",
    "🍰 Dessert Outing",
    "🍻 Drinks / Happy Hour"
]

activity_vibes = [
    "🎲 Board Games",
    "🎬 Movie Night",
    "🌳 Nature Walks",
    "🏖️ Beach Day",
    "🎭 Cultural Events",
    "🧠 Trivia Games",
    "🧩 Virtual Game Night",
    "🚴 Adventure Sports",
    "🍽️ Foodie Adventures"
]

all_vibes = meal_vibes + activity_vibes

selected_preferences = st.multiselect(
    "What kind of vibe is your group going for?",
    options=all_vibes
)
veto = st.selectbox("Anything you'd veto?", ["None"] + selected_preferences)

# Step 3: Generate AI Suggestions
st.header("Step 3: Suggestions")

if st.button("Regenerate Suggestions"):
    vibe_context = ", ".join(selected_preferences) if selected_preferences else "anything fun"
    prompt = f"""
    This group includes {user_name} in {user_city}.
    They're planning for {'a future meetup' if future_plan == 'Future' else 'now'}.
    The group is in the mood for: {vibe_context}.
    Veto: {veto if veto != "None" else "None"}.
    Suggest a few creative group activities or destinations that match the mood.
    Include food-related ideas if relevant. Keep the tone casual and group-friendly.
    """

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}]
    )
    ai_result = response.choices[0].message.content
    st.success("Here’s what the AI suggests:")
    st.markdown(ai_result)

    # Optional Real-time suggestions
    st.subheader("🔎 Explore Local Options")
    if plan_type in ["In-person", "Hybrid"]:
        query = selected_preferences[0].split(" ", 1)[-1] if selected_preferences else "food"
        results = search_foursquare_places(query, user_city, FOURSQUARE_API_KEY)
        for place in results:
            st.markdown(f"**{place['name']}**")
            st.caption(f"{place['address']} • {place['category']}")
            if place['url']:
                st.write(f"[View on Foursquare]({place['url']})")
            st.markdown("---")

    # Save session (optional CSV)
    user_data = [{
        "name": user_name,
        "email": user_email,
        "city": user_city,
        "preferences": selected_preferences,
        "veto": veto
    }]
    save_session_to_csv("vibepick_sessions.csv", st.session_state["session_id"], user_data, ai_result)

    # Email results
    if st.button("Email this to me"):
        subject = "Your VibePick Group Plan"
        send_email(MAILERSEND_API_KEY, user_email, subject, ai_result)
        st.success("Email sent!")
