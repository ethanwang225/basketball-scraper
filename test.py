import requests
from dotenv import load_dotenv
import os
import certifi

# Replace with your proxy user credentials.
load_dotenv()
username=os.getenv("PROXY_USERNAME")
password=os.getenv("PROXY_PASSWORD")

# Port `8000` rotates IPs from your proxy list.
address = 'dc.oxylabs.io:8000'

proxies = {
   'https': f'https://user-{username}:{password}@{address}'
}

response = requests.get('https://ip.oxylabs.io/location', proxies=proxies, verify=certifi.where())

print(response.text)