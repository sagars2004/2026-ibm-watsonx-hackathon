import os
import requests
from dotenv import load_dotenv

load_dotenv()

CLOUDANT_URL = os.getenv("CLOUDANT_URL")
CLOUDANT_API_KEY = os.getenv("CLOUDANT_API_KEY")

print("🔄 Testing IAM Authentication Flow...")

# Step 1: Exchange API Key for Token
print("Step 1: Requesting Access Token from IBM IAM...")
iam_url = "https://iam.cloud.ibm.com/identity/token"
headers = {"Content-Type": "application/x-www-form-urlencoded"}
data = {
    "grant_type": "urn:ibm:params:oauth:grant-type:apikey",
    "apikey": CLOUDANT_API_KEY
}

try:
    iam_res = requests.post(iam_url, headers=headers, data=data)
    
    if iam_res.status_code == 200:
        token = iam_res.json()["access_token"]
        print("✅ SUCCESS: Got Access Token!")
    else:
        print(f"❌ IAM FAILED: {iam_res.status_code}")
        print(iam_res.text)
        exit(1)

    # Step 2: Connect to Cloudant using Token
    print("\nStep 2: Connecting to Cloudant with Token...")
    # Cloudant URL usually ends with ...appdomain.cloud, we append the DB name
    db_name = "bottleneck_detector"
    db_url = f"{CLOUDANT_URL}/{db_name}"
    
    # Auth header is now "Bearer <token>"
    db_headers = {"Authorization": f"Bearer {token}"}
    
    db_res = requests.get(db_url, headers=db_headers)
    
    if db_res.status_code == 200:
        print(f"✅ SUCCESS! Connected to DB '{db_name}'")
        print(f"Docs: {db_res.json().get('doc_count')}")
    elif db_res.status_code == 404:
        print(f"⚠️ Authenticated! But DB '{db_name}' not found.")
        print("Creating it now...")
        create_res = requests.put(db_url, headers=db_headers)
        if create_res.status_code in [201, 202]:
             print(f"✅ SUCCESS! Created DB '{db_name}'")
        else:
             print(f"❌ Failed to create DB: {create_res.status_code}")
    else:
        print(f"❌ Cloudant Error: {db_res.status_code}")
        print(db_res.text)

except Exception as e:
    print(f"❌ EXCEPTION: {e}")
