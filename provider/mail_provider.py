import requests


def send_email(user_data):
    # url = "https://rapidmail.p.rapidapi.com/"
    url = "https://jsonplaceholder.typicode.com/posts"
    payload = {
        "ishtml": "false",
        "replyto": "",
        "title": "Validate your Account!",
        "body": "",
        **user_data
    }
    headers = {
        "content-type": "application/json",
        "X-RapidAPI-Key": "8f87677534msh19bf4365c6035dfp11a55djsnf848907a92b9",
        "X-RapidAPI-Host": "rapidmail.p.rapidapi.com"
    }

    return requests.post(url, json=payload, headers=headers).json()
