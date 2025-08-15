import firebase_admin
from firebase_admin import credentials, db, firestore
from datetime import datetime
import os
# --- Firebase Setup ---
# cred = credentials.Certificate("/Users/panashe/workplace/2025/Vimbai/utils/firebase-service-account.json")  # Path to your Firebase service account JSON
# firebase_admin.initialize_app(cred)
# db = firestore.client()


SERVICE_ACCOUNT_PATH = os.getenv(
    "FIREBASE_SERVICE_ACCOUNT", 
    "./utils/firebase-service-account.json"
)
cred = credentials.Certificate(SERVICE_ACCOUNT_PATH)
firebase_admin.initialize_app(cred)
db = firestore.client()
        
def post_to_firestore(data):
    # Format today's date as YYYY-MM-DD
    today_str = datetime.now().strftime("%Y-%m-%d")
    
    # Save to Firestore: categorized_articles/{today_str}
    db.collection("categorized_articles").document(today_str).set(data)
    print(f"✅ Data posted to Firestore at categorized_articles/{today_str}")
    
    
def get_categories_for_today():
    today_str = datetime.now().strftime("%Y-%m-%d")
    doc = db.collection("categorized_articles").document(today_str).get()
    if doc.exists:
        return doc.to_dict()  # returns categories + data
    else:
        print("⚠ No data found for today.")
        return {}
    
# post_to_firestore({"name":"panashe", "message":"testing"})