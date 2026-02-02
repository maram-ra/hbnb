# HBnB -- Holberton School Project (Part 4)

HBnB is a mini Airbnb-inspired full-stack web application built as part
of the Holberton School program. The project demonstrates integration
between a Flask REST API and a frontend built with HTML, CSS, and
JavaScript. Users can browse places, view details, log in, and add
reviews.

------------------------------------------------------------------------

## Overview

This project focuses on:

-   Building a REST API using Flask\
-   Connecting a frontend to backend endpoints\
-   Handling authentication with tokens\
-   Rendering dynamic content on the client side\
-   Managing CORS for local development

The backend uses mock in-memory data to simulate users, places, and
reviews.

------------------------------------------------------------------------

## Features

-   Browse a list of places\
-   View detailed information about a specific place\
-   Display amenities and reviews per place\
-   Filter places by price (client-side)\
-   Login with a demo user\
-   Add a review to a place (authenticated users only)\
-   Health check endpoint for the API

------------------------------------------------------------------------

## Tech Stack

### Backend

-   Python\
-   Flask 3.0.3\
-   Flask-CORS 4.0.1

### Frontend

-   HTML5\
-   CSS3\
-   JavaScript (Vanilla)\
-   Bootstrap 5 (CDN)\
-   Bootstrap Icons\
-   Google Fonts (Montserrat)

------------------------------------------------------------------------

## Project Structure

part4/ ├── backend/ │ ├── app.py │ └── requirements.txt │ ├── frontend/
│ ├── index.html │ ├── login.html │ ├── place.html │ ├── add_review.html
│ ├── scripts.js │ ├── styles.css │ ├── images/ │ └── videos/ └──
README.md

------------------------------------------------------------------------

## API Base URL

http://127.0.0.1:5000/api/v1

------------------------------------------------------------------------

## API Endpoints

  Method   Endpoint                Description                     Authentication
  -------- ----------------------- ------------------------------- ----------------
  POST     /login                  Login and return a demo token   No
  GET      /places                 List all places                 No
  GET      /places/`<id>`{=html}   Get place details + reviews     No
  POST     /reviews                Add a review                    Yes (Bearer)
  GET      /health                 Health check                    No

------------------------------------------------------------------------

## Authentication

The login endpoint returns a demo access token:

access_token: demo-token

The frontend stores the token in a cookie named `token`.\
Authenticated requests include the header:

Authorization: Bearer demo-token

### Demo User

Email: demo@hbnb.io\
Password: secret

------------------------------------------------------------------------

## Running the Project Locally

### 1. Start the Backend

cd backend\
python -m venv venv\
venv`\Scripts`{=tex}`\activate `{=tex}(Windows)\
source venv/bin/activate (Mac/Linux)

pip install -r requirements.txt\
python app.py

API runs at: http://127.0.0.1:5000

------------------------------------------------------------------------

### 2. Start the Frontend

Option A -- VS Code Live Server\
Open the frontend folder and run index.html with Live Server

Option B -- Python HTTP Server\
cd frontend\
python -m http.server 5500

Open: http://127.0.0.1:5500/index.html

------------------------------------------------------------------------

## Testing

1.  Start backend\
2.  Start frontend\
3.  Login with demo user\
4.  Browse places\
5.  View place details\
6.  Add review

------------------------------------------------------------------------

## Notes

-   Data is stored in memory and resets on server restart\
-   Focus is on API integration and authentication flow

------------------------------------------------------------------------

## Author

Maram -- Holberton School (Tuwaiq Academy)
