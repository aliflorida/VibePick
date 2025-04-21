
import streamlit as st
from openai import OpenAI
import uuid
from datetime import date
from place_search_utils import search_foursquare_places
from trip_cost_utils import search_trip_costs
from send_email_utils import send_email
from data_export import save_session_to_csv
from firebase_utils import (
    init_firebase,
    save_user_to_session,
    save_trip_to_session,
    get_session_users,
    get_trip_data
)

# Initialize Firebase
init_firebase(
    st.secrets["FIREBASE_CREDENTIALS"],
    st.secrets["FIREBASE_PROJECT_ID"],
    st.secrets["FIREBASE_DB_URL"]
)

# App Config
st.set_page_config(page_title="VibePick", layout="centered")
st.title("🎉 VibePick")
st.caption("Decide together. Pick your vibe.")

# Session setup
st.subheader("🔐 Group Session")
use_existing = st.radio("Are you starting or joining a session?", ["Start new", "Join existing"])
if use_existing == "Start new":
    session_id = str(uuid.uuid4())[:8]
    st.success(f"Your session code: `{session_id}` (share this with others)")
else:
    session_id = st.text_input("Enter your group's session code:")

if not session_id:
    st.stop()

# Step 1: Group Info
st.header("Step 1: Group Info")
user_name = st.text_input("Your name:")
user_email = st.text_input("Your email:")
user_city = st.text_input("Your city/location:")

# Trip planning toggle
trip_mode = st.checkbox("Are you planning a group trip?")
trip_data = {}

if trip_mode:
    st.subheader("✈️ Group Trip Planner")
    destination = st.text_input("Where are you planning to go?")
    trip_dates = st.date_input("Trip dates:", [])
    num_people = st.slider("How many are traveling?", 1, 10, 3)
    origins = [st.text_input(f"Where is person {i+1} traveling from?") for i in range(num_people)]
    trip_data = {
        "destination": destination,
        "origins": origins,
        "dates": [str(d) for d in trip_dates]
    }
    if destination:
        save_trip_to_session(session_id, trip_data)

# Step 2: Group Vibe
st.header("Step 2: Group Vibe")

meal_vibes = [
    "🍳 Breakfast", "🥪 Lunch", "🍝 Dinner", "🥂 Brunch",
    "🍕 Late-Night Eats", "🍰 Dessert Outing", "🍻 Drinks / Happy Hour"
]

activity_vibes = [
    "🎲 Board Games", "🎬 Movie Night", "🌳 Nature Walks", "🏖️ Beach Day",
    "🎭 Cultural Events", "🧠 Trivia Games", "🧩 Virtual Game Night",
    "🚴 Adventure Sports", "🍽️ Foodie Adventures"
]

all_vibes = meal_vibes + activity_vibes

selected_preferences = st.multiselect("What kind of vibe is your group going for?", options=all_vibes)
veto = st.selectbox("Anything you'd veto?", ["None"] + selected_preferences)

# Save user data to Firebase
if user_name and user_email:
    user_data = {
        "name": user_name,
        "email": user_email,
        "city": user_city,
        "preferences": selected_preferences,
        "veto": veto
    }
    save_user_to_session(session_id, user_data)

# Step 3: Generate AI Suggestions
st.header("Step 3: Suggestions")

if st.button("Regenerate Suggestions"):
    users = get_session_users(session_id)
    trip = get_trip_data(session_id)

    if not users:
        st.warning("No users found in session.")
        st.stop()

    group_names = ", ".join([user["name"] for user in users.values()])
    cities = ", ".join([user["city"] for user in users.values() if user.get("city")])
    all_prefs = set()
    all_vetoes = set()

    for u in users.values():
        all_prefs.update(u.get("preferences", []))
        if u.get("veto") and u["veto"] != "None":
            all_vetoes.add(u["veto"])

    vibe_context = ", ".join(all_prefs) if all_prefs else "fun group activities"
    veto_context = ", ".join(all_vetoes) if all_vetoes else "None"

    prompt = f"""
    This group includes: {group_names}, from: {cities}.
    The group vibe includes: {vibe_context}.
    Group vetoes: {veto_context}.
    {'They are planning a trip to ' + trip.get('destination') if trip else ''}
    Suggest creative group activities or travel ideas. Keep it casual and fun.
    """

    client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}]
    )
    ai_result = response.choices[0].message.content
    st.success("Here’s what the AI suggests:")
    st.markdown(ai_result)

    # Optional real-time search
    st.subheader("🔎 Explore Local Options")
    city_for_search = user_city or cities.split(",")[0]
    query = next(iter(all_prefs), "fun")
    results = search_foursquare_places(query, city_for_search, st.secrets["FOURSQUARE_API_KEY"])
    for place in results:
        st.markdown(f"**{place['name']}**")
        st.caption(f"{place['address']} • {place['category']}")
        if place['url']:
            st.write(f"[View on Foursquare]({place['url']})")
        st.markdown("---")

    # Travel price estimates
    if trip:
        st.subheader("💸 Estimated Travel Costs")
        for origin in trip.get("origins", []):
            st.markdown(f"**From {origin} to {trip['destination']}**")
            results = search_trip_costs(origin, trip["destination"], trip["dates"][0], trip["dates"][-1], st.secrets["SERPAPI_KEY"])
            for r in results[:2]:
                st.markdown(f"- {r['title']} [🔗]({r['link']})")

    # Email result to self
    if st.button("Email this to me"):
        send_email(st.secrets["MAILERSEND_API_KEY"], user_email, "Your VibePick Plan", ai_result)
        st.success("Email sent!")
