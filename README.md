# AI Travel Partner ✈️

An AI-powered full-stack travel companion app that generates personalized itineraries, recommends destinations, estimates budgets, and suggests local food — built with React + Flask + Groq AI (LLaMA 3.3 70B).

---

## Prerequisites

- Python 3.9+
- Node.js 18+
- A **Groq API Key** (free) — see below

---

## Step 1 — Get a Groq API Key (Free)

1. Go to [https://console.groq.com](https://console.groq.com)
2. Sign up for a free account
3. Go to **API Keys** → click **Create API Key**
4. Copy the key (starts with `gsk_...`)

---

## Step 2 — Setup Backend

```bash
cd backend
pip install -r requirements.txt
```

Create a `.env` file inside the `backend/` folder:

```
GROQ_API_KEY=your_groq_api_key_here
SECRET_KEY=travel-partner-secret-key-2026
JWT_SECRET=travel-jwt-secret-2026
```

Run the backend:

```bash
python app.py
```

Backend will start at `http://localhost:5000`

---

## Step 3 — Setup Frontend

```bash
cd frontend
npm install --legacy-peer-deps
npm start
```

Frontend will start at `http://localhost:3000`

---

## Step 4 — Open the App

Open your browser and go to:
```
http://localhost:3000
```

---

## Demo Accounts

| Role  | Email               | Password |
|-------|---------------------|----------|
| User  | user@travel.com     | user123  |
| Admin | admin@travel.com    | admin123 |

---

## Tech Stack

| Layer    | Technology                     |
|----------|--------------------------------|
| Frontend | React 18, React Router, Axios  |
| Backend  | Flask, Flask-SQLAlchemy, PyJWT |
| Database | SQLite                         |
| AI Model | Groq API — LLaMA 3.3 70B       |
| Auth     | JWT Tokens                     |
