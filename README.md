# AI Travel Partner ✈️

An AI-powered full-stack travel companion app that generates personalized itineraries, recommends destinations, estimates budgets, and suggests local food — built with React + Flask + Groq AI (LLaMA 3.3 70B).

---

## Get a Groq API Key (Free)

1. Go to [https://console.groq.com](https://console.groq.com)
2. Sign up for a free account
3. Go to **API Keys** → click **Create API Key**
4. Copy the key (starts with `gsk_...`)

---

## Option 1 — Run Locally

### Prerequisites
- Python 3.9+
- Node.js 18+

### Backend

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

Backend starts at `http://localhost:5000`

### Frontend

```bash
cd frontend
npm install --legacy-peer-deps
npm start
```

Frontend starts at `http://localhost:3000`

---

## Option 2 — Run with Docker

> Docker Images: [https://hub.docker.com/repository/docker/klmanasa/ai_travel_planner](https://hub.docker.com/repository/docker/klmanasa/ai_travel_planner)

### Prerequisites
- [Docker Desktop](https://www.docker.com/products/docker-desktop) installed and running

### Step 1 — Pull the Images

```bash
docker pull klmanasa/ai_travel_planner:backend
docker pull klmanasa/ai_travel_planner:frontend
```

### Step 2 — Start the Backend

Replace `your_groq_api_key_here` with your Groq API key.

**Windows (Command Prompt):**
```cmd
docker run -d --name ai-travel-backend -p 5000:5000 ^
  -e GROQ_API_KEY=your_groq_api_key_here ^
  -e SECRET_KEY=travel-partner-secret-key-2026 ^
  -e JWT_SECRET=travel-jwt-secret-2026 ^
  klmanasa/ai_travel_planner:backend
```

**Mac / Linux:**
```bash
docker run -d --name ai-travel-backend -p 5000:5000 \
  -e GROQ_API_KEY=your_groq_api_key_here \
  -e SECRET_KEY=travel-partner-secret-key-2026 \
  -e JWT_SECRET=travel-jwt-secret-2026 \
  klmanasa/ai_travel_planner:backend
```

### Step 3 — Start the Frontend

```bash
docker run -d --name ai-travel-frontend -p 3000:80 klmanasa/ai_travel_planner:frontend
```

### Step 4 — Open the App

```
http://localhost:3000
```

### Stop / Start / Reset

```bash
# Stop
docker stop ai-travel-backend ai-travel-frontend

# Start again
docker start ai-travel-backend ai-travel-frontend

# Remove and re-run fresh
docker rm -f ai-travel-backend ai-travel-frontend
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
