
# HBnB Part 4 - Simple Mock API (Flask)

Run locally at `http://127.0.0.1:5000/api/v1`.

## Quick start
```bash
python -m venv venv
# Windows
venv\Scripts\activate
# macOS/Linux
# source venv/bin/activate

pip install -r requirements.txt
python app.py
```

## Test credentials
- email: demo@hbnb.io
- password: secret

## Endpoints
- POST /api/v1/login
- GET  /api/v1/places
- GET  /api/v1/places/<id>
- POST /api/v1/reviews   (requires Authorization: Bearer demo-token)
