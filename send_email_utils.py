
import requests

def send_email(sendgrid_key, to_email, subject, content):
    url = "https://api.mailersend.com/v1/email"
    headers = {
        "Authorization": f"Bearer {sendgrid_key}",
        "Content-Type": "application/json"
    }
    data = {
        "from": {
            "email": "noreply@groupiedecisions.com",
            "name": "VibePick"
        },
        "to": [
            {"email": to_email}
        ],
        "subject": subject,
        "text": content
    }
    response = requests.post(url, headers=headers, json=data)
    return response.status_code == 202
