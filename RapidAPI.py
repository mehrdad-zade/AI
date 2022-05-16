import Secrets
import requests

"""
subscription to RapidAPI is required
"""

url = "https://japerk-text-processing.p.rapidapi.com/phrases/"

payload = "language=spanish&text=California%20is%20nice"
headers = {
    "content-type": "application/x-www-form-urlencoded",
    "X-RapidAPI-Host": Secrets.X_RapidAPI_Host,
    "X-RapidAPI-Key": Secrets.X_RapidAPI_Key
}

response = requests.request("POST", url, data=payload, headers=headers)
text = 'elon musk'
print(response.text)