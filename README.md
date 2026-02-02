# HBnB -- Holberton School Project (Part 4)

HBnB is a mini Airbnb-inspired full-stack web application built as part
of the Holberton School program. The project demonstrates integration
between a Flask REST API and a frontend built with HTML, CSS, and
JavaScript. Users can browse places, view details, log in, and add
reviews.

------------------------------------------------------------------------

## Overview

This project focuses on:

-   Building a REST API using Flask
-   Connecting a frontend to backend endpoints
-   Handling authentication with tokens
-   Rendering dynamic content on the client side
-   Managing CORS for local development

The backend uses mock in-memory data to simulate users, places, and
reviews.

------------------------------------------------------------------------

## Features

-   Browse a list of places
-   View detailed information about a specific place
-   Display amenities and reviews per place
-   Filter places by price (client-side)
-   Login with a demo user
-   Add a review to a place (authenticated users only)
-   Health check endpoint for the API

------------------------------------------------------------------------

## Tech Stack

### Backend

-   Python
-   Flask 3.0.3
-   Flask-CORS 4.0.1

### Frontend

-   HTML5
-   CSS3
-   JavaScript 
-   Bootstrap 5 



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

## Notes

-   Data is stored in memory and resets on server restart\
-   Focus is on API integration and authentication flow

------------------------------------------------------------------------

## Author

Maram -- Holberton School (Tuwaiq Academy)
