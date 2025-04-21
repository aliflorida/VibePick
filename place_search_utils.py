
import requests

def search_foursquare_places(query, location, fsq_api_key, limit=5):
    url = "https://api.foursquare.com/v3/places/search"
    headers = {
        "Authorization": fsq_api_key,
        "accept": "application/json"
    }
    params = {
        "query": query,
        "near": location,
        "limit": limit
    }

    response = requests.get(url, headers=headers, params=params)
    if response.status_code == 200:
        results = response.json().get("results", [])
        formatted = []
        for place in results:
            name = place.get("name")
            location = place.get("location", {})
            address = location.get("formatted_address", "No address")
            category = place.get("categories", [{}])[0].get("name", "No category")
            link = f"https://foursquare.com/v/{place.get('fsq_id')}" if place.get("fsq_id") else ""
            formatted.append({
                "name": name,
                "address": address,
                "category": category,
                "url": link
            })
        return formatted
    else:
        return []
