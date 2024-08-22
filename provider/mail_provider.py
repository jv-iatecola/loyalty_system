import requests


def send_email(user_data):
    url = "https://rapidmail.p.rapidapi.com/"
    # url = "https://jsonplaceholder.typicode.com/posts"
    payload = {
        "ishtml": "false",
        "replyto": "",
        "title": "Validate your Account!",
        **user_data
    }
    headers = {
        "x-rapidapi-key": "14d61413bbmsh2ec4e9c564c55fbp16950ejsn883b19105278",
        "x-rapidapi-host": "rapidmail.p.rapidapi.com",
        "Content-Type": "application/json"
    }

    return requests.post(url, json=payload, headers=headers).json()
