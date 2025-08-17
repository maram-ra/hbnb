
from flask import Flask, request, jsonify
from flask_cors import CORS
import uuid
import time

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": ["http://127.0.0.1:5500", "http://localhost:5500", "*"]}})

API_PREFIX = "/api/v1"

# ===== Mock DB =====
USERS = {
    "demo@hbnb.io": {"password": "secret", "first_name": "maram", "last_name": ""}
}

PLACES = [
    {
        "id": "a1",
        "title": "Ocean View Cabin",
        "price": 120,
        "description": "Relaxing cabin with ocean view.",
        "latitude": 24.7136,
        "longitude": 46.6753,
        "host": "John Doe",
        "country": "SA",
        "city": "Riyadh",
        "amenities": ["Wifi", "Air conditioning", "Kitchen"],
        "images": ["images/sample1.jpg"]
    },
    {
        "id": "b2",
        "title": "Mountain Retreat",
        "price": 98,
        "description": "Cozy escape in the mountains",
        "latitude": 36.7783,
        "longitude": -119.4179,
        "host": "Jane Smith",
        "country": "US",
        "city": "Fresno",
        "amenities": ["Heating", "Parking"],
        "images": ["images/sample2.jpg"]
    }
    
]

REVIEWS = [
    {"id": "r1", "place_id": "a1", "user": "reemah", "rating": 5, "comment": "Amazing view!"},
    {"id": "r2", "place_id": "a1", "user": "osama", "rating": 4, "comment": "Very cozy."},
]

# ===== Helpers =====
DEMO_TOKEN = "demo-token"

def get_token_from_header():
    auth = request.headers.get("Authorization", "")
    if auth.startswith("Bearer "):
        return auth.split(" ", 1)[1].strip()
    return None

def require_auth():
    token = get_token_from_header()
    return token == DEMO_TOKEN

def serialize_place(p):
    # Attach reviews for the place
    reviews = [r for r in REVIEWS if r["place_id"] == p["id"]]
    return {
        "id": p["id"],
        "title": p["title"],
        "price": p["price"],
        "description": p["description"],
        "latitude": p["latitude"],
        "longitude": p["longitude"],
        "host": p["host"],
        "country": p.get("country"),
        "city": p.get("city"),
        "amenities": p.get("amenities", []),
        "images": p.get("images", []),
        "reviews": reviews,
    }

# ===== Routes =====
@app.post(f"{API_PREFIX}/login")
def login():
    data = request.get_json(force=True, silent=True) or {}
    email = data.get("email", "").strip().lower()
    password = data.get("password", "")

    user = USERS.get(email)
    if not user or user["password"] != password:
        return jsonify({"message": "Invalid credentials"}), 401

    return jsonify({
        "access_token": DEMO_TOKEN,
        "token_type": "bearer",
        "expires_in": 3600,
        "user": {
            "email": email,
            "first_name": user["first_name"],
            "last_name": user["last_name"]
        }
    }), 200

@app.get(f"{API_PREFIX}/places")
def list_places():
    places = [serialize_place(p) for p in PLACES]
    return jsonify(places), 200

@app.get(f"{API_PREFIX}/places/<place_id>")
def place_details(place_id):
    place = next((p for p in PLACES if p["id"] == place_id), None)
    if not place:
        return jsonify({"message": "Place not found"}), 404
    return jsonify(serialize_place(place)), 200

@app.post(f"{API_PREFIX}/reviews")
def add_review():
    if not require_auth():
        return jsonify({"message": "Unauthorized"}), 401

    data = request.get_json(force=True, silent=True) or {}
    place_id = data.get("place_id")
    comment = data.get("comment") or data.get("text")
    rating = data.get("rating", 5)

    if not place_id or not comment:
        return jsonify({"message": "place_id and comment are required"}), 400

    if not any(p["id"] == place_id for p in PLACES):
        return jsonify({"message": "Place not found"}), 404

    new_review = {
        "id": str(uuid.uuid4())[:8],
        "place_id": place_id,
        "user": "maram",
        "rating": rating,
        "comment": comment,
        "created_at": int(time.time())
    }
    REVIEWS.append(new_review)
    return jsonify(new_review), 201

@app.get(f"{API_PREFIX}/health")
def health():
    return jsonify({"status": "ok"}), 200

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)
