
# virtual_event_utils.py
import requests
import os

EVENTBRITE_TOKEN = os.getenv("EVENTBRITE_TOKEN")
SERPAPI_KEY = os.getenv("SERPAPI_KEY")
FOURSQUARE_API_KEY = os.getenv("FOURSQUARE_API_KEY")

def search_eventbrite_events(keywords):
    headers = {"Authorization": f"Bearer {EVENTBRITE_TOKEN}"}
    query = ",".join(keywords)
    url = f"https://www.eventbriteapi.com/v3/events/search/?q={query}&online_event=true"
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        data = response.json()
        return [{
            "name": e["name"]["text"],
            "url": e["url"],
            "date": e["start"]["local"].split("T")[0]
        } for e in data.get("events", [])]
    except:
        return []

def search_foursquare_places(keywords, location="New York"):
    try:
        url = "https://api.foursquare.com/v3/places/search"
        headers = {
            "Authorization": FOURSQUARE_API_KEY,
            "Accept": "application/json"
        }
        params = {
            "query": ",".join(keywords),
            "near": location,
            "limit": 5
        }
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        data = response.json()
        return [{
            "name": place["name"],
            "url": f"https://foursquare.com/v/{place['fsq_id']}",
            "date": "Local"
        } for place in data.get("results", [])]
    except:
        return []

def search_meta_vr_events():
    try:
        response = requests.get("https://www.meta.com/events/")
        return [{"name": "Meta VR Event", "url": "https://www.meta.com/events/", "date": "Upcoming"}]
    except:
        return []

def search_apple_vision_events():
    try:
        response = requests.get("https://www.apple.com/apple-vision-pro/")
        return [{"name": "Apple Vision Pro Showcase", "url": "https://www.apple.com/apple-vision-pro/", "date": "Ongoing"}]
    except:
        return []

def search_serpapi_events(keywords):
    url = "https://serpapi.com/search"
    query = ",".join(keywords)
    params = {
        "q": f"{query} virtual events site:meetup.com OR site:eventbrite.com OR site:meta.com OR site:apple.com",
        "api_key": SERPAPI_KEY,
        "engine": "google"
    }
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        results = response.json()
        return [{
            "name": r["title"],
            "url": r["link"],
            "date": "N/A"
        } for r in results.get("organic_results", [])]
    except:
        return []

def search_virtual_events(keywords, location="New York"):
    if not keywords:
        return []

    all_events = []
    all_events.extend(search_eventbrite_events(keywords))
    all_events.extend(search_foursquare_places(keywords, location))
    all_events.extend(search_meta_vr_events())
    all_events.extend(search_apple_vision_events())
    all_events.extend(search_serpapi_events(keywords))
    return all_events
