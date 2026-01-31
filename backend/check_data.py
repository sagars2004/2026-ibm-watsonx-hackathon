import os
import requests
import json
from dotenv import load_dotenv

load_dotenv()

CLOUDANT_URL = os.getenv("CLOUDANT_URL")
CLOUDANT_API_KEY = os.getenv("CLOUDANT_API_KEY")
CLOUDANT_DB_NAME = os.getenv("CLOUDANT_DB_NAME", "bottleneck_detector")

def get_token():
    iam_url = "https://iam.cloud.ibm.com/identity/token"
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    data = {
        "grant_type": "urn:ibm:params:oauth:grant-type:apikey",
        "apikey": CLOUDANT_API_KEY
    }
    res = requests.post(iam_url, headers=headers, data=data)
    return res.json()["access_token"]

try:
    token = get_token()
    url = f"{CLOUDANT_URL}/{CLOUDANT_DB_NAME}/latest_analysis"
    headers = {"Authorization": f"Bearer {token}"}
    
    res = requests.get(url, headers=headers)
    data = res.json()
    
    jira_blocked = data["jira"]["summary"]["blocked_count"]
    print(f"\n📢 CURRENT DB VAlUE: Blocked Count = {jira_blocked}\n")
    
except Exception as e:
    print(e)
