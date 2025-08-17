
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
        "id": "c3",
        "title": "Desert Eco ",
        "price": 150,
        "description": "Sustainable dome in the heart of the desert.",
        "latitude": 24.7743,
        "longitude": 46.7386,
        "host": "Salma",
        "country": "SA",
        "city": "AlUla",
        "amenities": ["Solar power", "AC", "Star view"],
        "images": ["images/sample4.jpg"]
    },
    {
        "id": "d4",
        "title": "Lakeside A-Frame",
        "price": 180,
        "description": "A modern cabin on the lake edge.",
        "latitude": 44.3148,
        "longitude": -85.6024,
        "host": "Khaled",
        "country": "US",
        "city": "Michigan",
        "amenities": ["Fireplace", "WiFi", "Canoe"],
        "images": ["images/sample3.jpg"]
    },
    {
        "id": "e5",
        "title": "Tropical Treehouse",
        "price": 210,
        "description": "Live among the trees in this tropical escape.",
        "latitude": 8.7832,
        "longitude": -55.4915,
        "host": "Fatima",
        "country": "BR",
        "city": "Manaus",
        "amenities": ["Outdoor shower", "Breakfast included"],
        "images": ["images/sample2.jpg"]
    },
    {
        "id": "f6",
        "title": "Scandinavian Loft",
        "price": 130,
        "description": "Minimalist loft in a Nordic city.",
        "latitude": 59.3293,
        "longitude": 18.0686,
        "host": "Sven",
        "country": "SE",
        "city": "Stockholm",
        "amenities": ["Sauna", "Fast WiFi", "City view"],
        "images": ["images/sample1.jpg"]
    }
    
]

REVIEWS = [
    {"id": "r3", "place_id": "c3", "user": "salem", "rating": 5, "comment": "Magical dome in the desert!"},
    {"id": "r4", "place_id": "d4", "user": "lena", "rating": 4, "comment": "Very peaceful by the lake."},
    {"id": "r5", "place_id": "e5", "user": "ahmad", "rating": 5, "comment": "The treehouse was dreamy!"},
    {"id": "r6", "place_id": "f6", "user": "sara", "rating": 3, "comment": "Loved the Scandinavian design."},

    {"id": "r7", "place_id": "c3", "user": "noura", "rating": 4, "comment": "A quiet and eco-friendly escape."},
    {"id": "r8", "place_id": "c3", "user": "jake", "rating": 5, "comment": "Stargazing at night was unforgettable."},

    {"id": "r9", "place_id": "d4", "user": "reem", "rating": 5, "comment": "Woke up to birds and lake mist — perfect!"},
    {"id": "r10", "place_id": "d4", "user": "mohammed", "rating": 4, "comment": "Comfortable and very scenic."},

    {"id": "r11", "place_id": "e5", "user": "laura", "rating": 5, "comment": "Nature all around — felt alive!"},
    {"id": "r12", "place_id": "e5", "user": "ali", "rating": 4, "comment": "Clean, cozy, and surrounded by trees."},

    {"id": "r13", "place_id": "f6", "user": "emily", "rating": 4, "comment": "Minimalist but super functional."},
    {"id": "r14", "place_id": "f6", "user": "abdullah", "rating": 5, "comment": "A hidden gem in Stockholm!"}
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
