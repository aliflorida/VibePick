
import csv
import os

def save_session_to_csv(filename, session_id, user_data, ai_result, trip_info=None):
    headers = [
        "session_id", "user_name", "email", "city", "preferences", "veto", "ai_result", 
        "trip_destination", "trip_origins", "trip_dates"
    ]

    file_exists = os.path.isfile(filename)

    with open(filename, mode="a", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=headers)
        if not file_exists:
            writer.writeheader()

        for user in user_data:
            row = {
                "session_id": session_id,
                "user_name": user.get("name"),
                "email": user.get("email"),
                "city": user.get("city"),
                "preferences": ", ".join(user.get("preferences", [])),
                "veto": user.get("veto"),
                "ai_result": ai_result,
                "trip_destination": trip_info.get("destination") if trip_info else "",
                "trip_origins": ", ".join(trip_info.get("origins", [])) if trip_info else "",
                "trip_dates": ", ".join(str(d) for d in trip_info.get("dates", [])) if trip_info else ""
            }
            writer.writerow(row)
