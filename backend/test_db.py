import os
import requests
from dotenv import load_dotenv

load_dotenv()

CLOUDANT_URL = os.getenv("CLOUDANT_URL")
CLOUDANT_API_KEY = os.getenv("CLOUDANT_API_KEY")
CLOUDANT_DB_NAME = os.getenv("CLOUDANT_DB_NAME", "bottleneck_detector")

print(f"Checking Cloudant Connection...")
print(f"URL: {CLOUDANT_URL}")
print(f"DB Name: {CLOUDANT_DB_NAME}")

if not CLOUDANT_URL or not CLOUDANT_API_KEY:
    print("❌ CREDENTIALS MISSING")
    exit(1)

base_url = f"{CLOUDANT_URL}/{CLOUDANT_DB_NAME}"
auth = ("apikey", CLOUDANT_API_KEY)

try:
    print("Attempting to connect...")
    res = requests.get(base_url, auth=auth)
    
    if res.status_code == 200:
        print(f"✅ SUCCESS! Connected to database '{CLOUDANT_DB_NAME}'")
        print(f"Doc count: {res.json().get('doc_count', 'unknown')}")
    elif res.status_code == 404:
        print(f"⚠️ Connected, but database '{CLOUDANT_DB_NAME}' DOES NOT EXIST.")
        print("Attempting to create it...")
        create_res = requests.put(base_url, auth=auth)
        if create_res.status_code in [201, 202]:
            print(f"✅ SUCCESS! Created database '{CLOUDANT_DB_NAME}'")
        else:
            print(f"❌ FAILED to create DB: {create_res.status_code} {create_res.text}")
    else:
        print(f"❌ ERROR: Status Code {res.status_code}")
        print(f"Response: {res.text}")

except Exception as e:
    print(f"❌ EXCEPTION: {e}")
