
import requests

def search_trip_costs(origin, destination, start_date, end_date, serpapi_key):
    query = f"flight from {origin} to {destination} on {start_date} returning {end_date}"
    url = "https://serpapi.com/search"
    params = {
        "q": query,
        "api_key": serpapi_key,
        "engine": "duckduckgo"
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        return response.json().get("organic_results", [])
    return []
