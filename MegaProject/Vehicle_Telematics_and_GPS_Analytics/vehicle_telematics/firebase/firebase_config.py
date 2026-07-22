import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

# Load the Firebase private key
cred = credentials.Certificate("firebase/firebase_key.json")

# Initialize Firebase only once
if not firebase_admin._apps:
    firebase_admin.initialize_app(cred)

# Create Firestore client
db = firestore.client()