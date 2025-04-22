
# virtual_event_utils.py
import requests
import os

EVENTBRITE_TOKEN = os.getenv("EVENTBRITE_TOKEN")

def search_virtual_events(activity_keywords):
    keyword_query = " ".join(activity_keywords)
    url = f"https://www.eventbriteapi.com/v3/events/search/?q={keyword_query}&online_event=true"

    headers = {
        "Authorization": f"Bearer {EVENTBRITE_TOKEN}"
    }

    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        return []

    events = response.json().get("events", [])
    results = []

    for e in events[:10]:
        results.append({
            "name": e.get("name", {}).get("text", "Unnamed Event"),
            "date": e.get("start", {}).get("local", "TBD"),
            "url": e.get("url", "#")
        })

    return results
