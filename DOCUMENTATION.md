# AI Travel Partner — Full Project Documentation

> Written for beginners. No prior experience needed to understand this.

---

## Table of Contents

1. [What is this project?](#1-what-is-this-project)
2. [How does the app look?](#2-how-does-the-app-look)
3. [Technologies used](#3-technologies-used)
4. [Project folder structure](#4-project-folder-structure)
5. [Frontend — What the user sees](#5-frontend--what-the-user-sees)
6. [Backend — The brain of the app](#6-backend--the-brain-of-the-app)
7. [Database — Where data is stored](#7-database--where-data-is-stored)
8. [AI Integration — How the AI works](#8-ai-integration--how-the-ai-works)
9. [API Endpoints — How frontend talks to backend](#9-api-endpoints--how-frontend-talks-to-backend)
10. [Authentication — How login works](#10-authentication--how-login-works)
11. [Docker — How we packaged the app](#11-docker--how-we-packaged-the-app)

---

## 1. What is this project?

**AI Travel Partner** is a web application that helps people plan their trips using Artificial Intelligence.

Instead of spending hours researching travel destinations, hotels, and activities — users simply tell the app where they want to go, their budget, and what they enjoy. The AI then automatically:

- Creates a **day-by-day itinerary** (schedule of activities for each day)
- Recommends **travel destinations** in India
- Estimates the **total trip budget** with a cost breakdown
- Suggests **local food** to try at the destination

Think of it like having a personal travel agent available 24/7 — powered by AI.

---

## 2. How does the app look?

The app has the following pages:

| Page | What it does |
|------|-------------|
| **Home** | Shows popular destinations, search bar |
| **Explore** | Browse and filter all destinations |
| **Food** | Get local food recommendations for any destination |
| **Plan Trip** | 3-step wizard to generate an AI travel plan |
| **Itinerary** | View the generated day-by-day travel plan |
| **Dashboard** | View all your saved trips |
| **Profile** | Edit your account details |
| **Login / Register** | Create account or log in |
| **Admin Dashboard** | Admin-only page to manage destinations and users |

The app works on both desktop and mobile. On mobile, there is a bottom navigation bar (like most mobile apps).

---

## 3. Technologies used

### What is a "tech stack"?
A tech stack is simply the list of tools and programming languages used to build an application.

### Frontend (what the user sees in the browser)

| Technology | What it is | Why we used it |
|-----------|-----------|---------------|
| **React 18** | A JavaScript library for building web pages | Makes it easy to build interactive UIs with reusable components |
| **React Router** | Handles navigation between pages | Users can move between pages without reloading the browser |
| **Axios** | Sends requests from frontend to backend | Simpler than the built-in browser fetch API |
| **CSS** | Styles the visual design | Controls colors, fonts, layout, and animations |

### Backend (the server that processes data)

| Technology | What it is | Why we used it |
|-----------|-----------|---------------|
| **Python** | Programming language | Easy to read and widely used for backend and AI |
| **Flask** | A lightweight web framework for Python | Simple to set up and great for building APIs |
| **Flask-SQLAlchemy** | Connects Flask to a database | Makes database operations easy without writing raw SQL |
| **PyJWT** | Handles JSON Web Tokens for login | Securely verifies who is logged in |
| **Flask-CORS** | Allows frontend to talk to backend | Browsers block cross-origin requests by default |

### AI

| Technology | What it is | Why we used it |
|-----------|-----------|---------------|
| **Groq API** | A free AI API service | Provides access to powerful AI models |
| **LLaMA 3.3 70B** | The AI language model | Understands travel prompts and generates detailed plans |

### Database

| Technology | What it is | Why we used it |
|-----------|-----------|---------------|
| **SQLite** | A simple file-based database | No setup needed, perfect for small/college projects |

### Deployment

| Technology | What it is | Why we used it |
|-----------|-----------|---------------|
| **Docker** | Packages the app into containers | Makes it easy to run on any machine without setup |
| **Nginx** | A web server | Serves the React frontend inside Docker |

---

## 4. Project folder structure

```
AI_Travel_Partner/
│
├── backend/                   → Python Flask server (the backend)
│   ├── app.py                 → Main entry point — starts the server
│   ├── config.py              → App settings (secret keys, database path)
│   ├── database.py            → Sets up the database and adds sample data
│   ├── utils.py               → Helper functions (JWT token creation/check)
│   ├── requirements.txt       → List of Python packages needed
│   ├── .env                   → Secret keys (NOT uploaded to GitHub)
│   │
│   ├── models/                → Database table definitions
│   │   ├── user.py            → User table (name, email, password)
│   │   ├── destination.py     → Destination table (name, state, category)
│   │   └── itinerary.py       → Trip/Itinerary table
│   │
│   ├── routes/                → API endpoints (URL handlers)
│   │   ├── auth.py            → /api/auth → login, register
│   │   ├── user.py            → /api/user → profile, trips
│   │   ├── destinations.py    → /api/destinations → browse destinations
│   │   ├── ai_routes.py       → /api/ai → all AI features
│   │   └── admin.py           → /api/admin → admin controls
│   │
│   └── ai_modules/            → (Legacy) Custom algorithm files
│       └── ...                → Replaced by Groq AI API calls
│
├── frontend/                  → React app (the frontend)
│   ├── public/
│   │   └── index.html         → The single HTML file React uses
│   │
│   └── src/
│       ├── App.js             → Main file — sets up all page routes
│       ├── index.css          → Global styles (colors, fonts, buttons)
│       │
│       ├── context/
│       │   └── AuthContext.js → Stores login state across all pages
│       │
│       ├── components/        → Reusable UI pieces
│       │   ├── Navbar.js      → Top navigation bar + mobile bottom nav
│       │   ├── Footer.js      → Page footer
│       │   └── ProtectedRoute.js → Blocks pages if not logged in
│       │
│       ├── pages/             → One file per page
│       │   ├── Home.js        → Home page
│       │   ├── Login.js       → Login page
│       │   ├── Register.js    → Register page
│       │   ├── Dashboard.js   → User dashboard with saved trips
│       │   ├── PlanTrip.js    → 3-step trip planner wizard
│       │   ├── Itinerary.js   → View generated itinerary
│       │   ├── Destinations.js→ Browse destinations
│       │   ├── Food.js        → Food recommendations page
│       │   ├── Profile.js     → User profile page
│       │   └── AdminDashboard.js → Admin management page
│       │
│       └── services/
│           └── api.js         → All API call functions (talks to backend)
│
├── README.md                  → How to run the project
├── PSEUDOCODE.md              → Logic explained in simple pseudocode
├── DOCUMENTATION.md           → This file
└── docker-compose.yml         → Runs both frontend and backend with Docker
```

---

## 5. Frontend — What the user sees

### How React works (simple explanation)
React breaks a webpage into small reusable pieces called **components**. For example, the Navbar is one component, each destination card is a component, and each page is a component. These components are combined to build the full page.

### Key files explained

**`App.js`** — This is the starting point of the frontend. It defines which page (component) shows up for each URL:
- `/` → Home page
- `/login` → Login page
- `/plan-trip` → Plan Trip page
- `/food` → Food Recommendations page
- and so on...

**`AuthContext.js`** — This stores the logged-in user's information (name, token) so that ALL pages in the app can access it. Without this, each page would forget who is logged in.

**`api.js`** — This file contains all the functions that talk to the backend. For example:
- `authApi.login(email, password)` → sends login request to backend
- `aiApi.generateItinerary(form)` → asks backend to generate a travel plan
- `userApi.saveTrip(data)` → saves a trip to the database

**`ProtectedRoute.js`** — This is a guard. If someone tries to visit `/dashboard` without being logged in, it automatically redirects them to the login page.

### Pages explained

**Home page** (`Home.js`)
- Shows the app title and a search bar
- Displays popular destination cards (Goa, Manali, etc.)
- Clicking a destination card takes the user to Plan Trip with that destination pre-filled

**Plan Trip page** (`PlanTrip.js`)
- Works in 3 steps:
  1. Enter destination, number of days, travelers, budget
  2. Choose interests, hotel type, transport mode
  3. AI generates the plan (loading screen shown)
- During Step 2, a live budget estimate is shown in a sidebar using the AI budget API

**Itinerary page** (`Itinerary.js`)
- Shows the full AI-generated travel plan
- Includes: budget breakdown bars, day-by-day schedule, meals, accommodation, travel tips
- Has a sidebar with highlights and trip info

**Food page** (`Food.js`)
- User types any destination
- AI returns a list of must-try local foods with name, description, price range, and emoji

**Dashboard** (`Dashboard.js`)
- Shows all trips the logged-in user has saved
- Also shows AI-recommended destinations based on user preferences

---

## 6. Backend — The brain of the app

### How Flask works (simple explanation)
Flask is a Python framework that creates a **web server**. This server listens for incoming requests from the frontend, processes them (e.g. saves to database, calls AI), and sends back a response.

Each URL the backend handles is called an **API endpoint**. For example:
- Frontend sends a POST request to `/api/auth/login` with email and password
- Backend checks the database, verifies the password, and returns a token

### Key files explained

**`app.py`** — Starts the Flask server and registers all the route blueprints (groups of API endpoints).

**`config.py`** — Stores settings like the database path, secret key for JWT tokens, and debug mode. Reads values from the `.env` file.

**`database.py`** — Creates the database tables when the server first starts, and fills them with sample data (12 Indian destinations and 2 demo user accounts).

**`utils.py`** — Contains helper functions:
- `generate_token(user_id)` → Creates a JWT token after login
- `decode_token(token)` → Reads a JWT token to get the user ID
- `token_required` → A decorator (guard) that protects API routes — checks if the request has a valid token

### Routes (API endpoint groups)

**`auth.py`** — Handles user accounts:
- Register a new user
- Login with email and password
- Get current logged-in user details

**`user.py`** — Handles user data:
- Get and update profile
- Get all saved trips
- Save a new trip
- Delete a trip

**`destinations.py`** — Handles destination data:
- Get all destinations
- Get a single destination by ID
- Add a review for a destination

**`ai_routes.py`** — All AI-powered features:
- Generate itinerary
- Recommend destinations
- Estimate budget
- Food recommendations
- Compare destinations

**`admin.py`** — Admin-only features:
- View app stats (total users, trips, destinations)
- Add, edit, delete destinations
- View all users

---

## 7. Database — Where data is stored

We use **SQLite** — a simple database stored as a single file (`backend/instance/travel_partner.db`). No separate database server is needed.

### Tables (think of these as spreadsheets)

**Users table**
| Column | Type | Description |
|--------|------|-------------|
| id | Integer | Unique ID for each user |
| name | String | Full name |
| email | String | Email address (must be unique) |
| password_hash | String | Encrypted password (never stored as plain text) |
| role | String | "user" or "admin" |
| preferences | JSON | Saved interests and budget preference |
| created_at | DateTime | When the account was created |

**Destinations table**
| Column | Type | Description |
|--------|------|-------------|
| id | Integer | Unique ID |
| name | String | Destination name (e.g. Goa) |
| state | String | Which state it's in |
| category | String | beach, mountain, city, etc. |
| description | Text | About the destination |
| base_cost_per_day | Float | Estimated daily cost |
| popular_attractions | JSON | List of famous places |
| best_season | String | Best time to visit |

**Trips (Itineraries) table**
| Column | Type | Description |
|--------|------|-------------|
| id | Integer | Unique ID |
| user_id | Integer | Which user created this trip |
| destination | String | Where the trip is to |
| days | Integer | Number of days |
| travelers | Integer | Number of travelers |
| plan | JSON | Full AI-generated itinerary |
| total_cost | Float | Estimated total cost |
| status | String | "planned", "completed", etc. |

### Sample data (pre-loaded)
When the app starts for the first time, it automatically adds:
- **12 destinations**: Goa, Manali, Ladakh, Jaipur, Kerala, Darjeeling, Ooty, Agra, Varanasi, Mumbai, Coorg, Andaman
- **2 demo users**: a regular user and an admin

---

## 8. AI Integration — How the AI works

### What is Groq?
Groq is a free AI API service (like OpenAI but free). We use it to access **LLaMA 3.3 70B** — a powerful AI language model made by Meta.

### How we send a request to the AI

Every AI feature follows the same 3 steps:

```
Step 1: Build a prompt
    → Write a detailed instruction to the AI in plain English
    → Include all the user's inputs (destination, budget, interests, etc.)

Step 2: Send to Groq API
    → Send an HTTP POST request to https://api.groq.com/openai/v1/chat/completions
    → Include the API key in the request header for authentication

Step 3: Parse the response
    → The AI replies with text
    → We extract the JSON from the text
    → Return the structured data to the frontend
```

### Example — Itinerary Generation prompt

We send the AI a message like:

> "Create a detailed 5-day travel itinerary for Goa, India. Travelers: 2. Budget: Rs 20000. Interests: beach, food. Hotel: standard. Transport: flight. Return a JSON object with day-by-day activities, meals, accommodation, and budget breakdown."

The AI responds with a complete JSON structure that we directly display in the Itinerary page.

### Why use AI instead of hardcoded data?
- AI gives **personalized** results based on each user's preferences
- AI knows about **real places, real restaurants, and real activities**
- AI can generate itineraries for **any destination** — not just pre-loaded ones
- Results feel natural and detailed, like advice from a real travel expert

### API Key security
The Groq API key is stored in the `.env` file (which is never uploaded to GitHub). Inside Docker, it is passed as an environment variable at runtime:
```
-e GROQ_API_KEY=your_key_here
```
This means the key is never exposed in the code.

---

## 9. API Endpoints — How frontend talks to backend

An **API endpoint** is a URL that the frontend calls to get or send data.

### Authentication
| Method | URL | What it does |
|--------|-----|-------------|
| POST | `/api/auth/register` | Create a new account |
| POST | `/api/auth/login` | Login and get a token |
| GET | `/api/auth/me` | Get current user details |

### User
| Method | URL | What it does |
|--------|-----|-------------|
| GET | `/api/user/profile` | Get user profile |
| PUT | `/api/user/profile` | Update profile |
| GET | `/api/user/trips` | Get all saved trips |
| POST | `/api/user/trips` | Save a new trip |
| DELETE | `/api/user/trips/<id>` | Delete a trip |

### Destinations
| Method | URL | What it does |
|--------|-----|-------------|
| GET | `/api/destinations/` | Get all destinations |
| GET | `/api/destinations/<id>` | Get one destination |
| POST | `/api/destinations/<id>/review` | Add a review |

### AI Features
| Method | URL | What it does |
|--------|-----|-------------|
| POST | `/api/ai/generate-itinerary` | Generate full trip plan |
| POST | `/api/ai/recommend-destinations` | Get destination suggestions |
| POST | `/api/ai/estimate-budget` | Estimate trip cost |
| POST | `/api/ai/food-recommendations` | Get local food suggestions |
| POST | `/api/ai/compare-destinations` | Compare two destinations |

### Admin
| Method | URL | What it does |
|--------|-----|-------------|
| GET | `/api/admin/stats` | Get app statistics |
| GET | `/api/admin/users` | Get all users |
| POST | `/api/admin/destinations` | Add a destination |
| PUT | `/api/admin/destinations/<id>` | Edit a destination |
| DELETE | `/api/admin/destinations/<id>` | Delete a destination |

---

## 10. Authentication — How login works

We use **JWT (JSON Web Tokens)** for authentication. Here's how it works step by step:

```
1. User enters email and password on the Login page

2. Frontend sends these to the backend (POST /api/auth/login)

3. Backend checks:
   - Does this email exist in the database?
   - Does the password match the stored encrypted password?

4. If correct, backend creates a JWT token:
   - The token contains the user's ID
   - It is signed with a secret key so it cannot be faked
   - It expires after 7 days

5. Backend sends the token back to the frontend

6. Frontend saves the token in the browser's localStorage

7. From now on, every API request from the frontend includes this token
   in the request header:
   Authorization: Bearer <token>

8. Backend checks this token on every protected route
   - If valid → process the request
   - If missing or expired → return "Unauthorized" error

9. When the user logs out:
   - Frontend deletes the token from localStorage
   - User is redirected to the login page
```

**Why not use passwords directly?**
Sending the password with every request would be insecure. A JWT token is a safer alternative — it proves the user is logged in without exposing their password.

---

## 11. Docker — How we packaged the app

### What is Docker?
Docker packages an application and everything it needs (Python, Node.js, libraries) into a **container** — like a sealed box. This box can run on any machine (Windows, Mac, Linux) without any setup.

### Our Docker setup

We have **2 containers**:

**Backend container** (`ai_travel_planner:backend`)
- Base image: Python 3.11
- Installs all Python packages from `requirements.txt`
- Copies all backend code
- Starts Flask server on port 5000

**Frontend container** (`ai_travel_planner:frontend`)
- Step 1 (Build stage): Uses Node.js 18 to build the React app into static HTML/CSS/JS files
- Step 2 (Serve stage): Uses Nginx web server to serve those static files on port 80
- This two-step approach keeps the final image small

### How to run with Docker
```bash
# Pull images from Docker Hub
docker pull klmanasa/ai_travel_planner:backend
docker pull klmanasa/ai_travel_planner:frontend

# Start backend (pass your Groq API key here)
docker run -d --name ai-travel-backend -p 5000:5000 \
  -e GROQ_API_KEY=your_key_here \
  klmanasa/ai_travel_planner:backend

# Start frontend
docker run -d --name ai-travel-frontend -p 3000:80 \
  klmanasa/ai_travel_planner:frontend

# Open browser at http://localhost:3000
```

### Docker Hub
Both images are publicly available at:
[https://hub.docker.com/repository/docker/klmanasa/ai_travel_planner](https://hub.docker.com/repository/docker/klmanasa/ai_travel_planner)

---

## Summary

| What | How |
|------|-----|
| User interface | React 18 with plain CSS |
| Server | Python Flask REST API |
| Database | SQLite (file-based, no server needed) |
| AI | Groq API with LLaMA 3.3 70B |
| Login system | JWT tokens |
| Deployment | Docker containers |
| Hosting images | Docker Hub (klmanasa/ai_travel_planner) |
| Source code | GitHub (manasa061210/AI-Travel-Partner) |

---

*Built as a college project — AI Enhanced Travel Companion*
