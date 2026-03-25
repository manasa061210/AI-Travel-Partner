# AI Travel Partner ✈️

An AI-powered full-stack travel companion app that generates personalized itineraries, recommends destinations, estimates budgets, and suggests local food — built with React + Flask + Groq AI (LLaMA 3.3 70B).

---

## Prerequisites

- [Docker Desktop](https://www.docker.com/products/docker-desktop) installed and running
- A **Groq API Key** (free) — see below

---

## Step 1 — Get a Groq API Key (Free)

1. Go to [https://console.groq.com](https://console.groq.com)
2. Sign up for a free account
3. Go to **API Keys** → click **Create API Key**
4. Copy the key (starts with `gsk_...`)

---

## Step 2 — Install Docker Desktop

1. Download from [https://www.docker.com/products/docker-desktop](https://www.docker.com/products/docker-desktop)
2. Install and restart your PC if prompted
3. Open Docker Desktop and wait until it shows **"Engine running"** in the bottom left

---

## Step 3 — Open Terminal / Command Prompt

- **Windows**: Press `Windows + R`, type `cmd`, press Enter
- **Mac**: Press `Cmd + Space`, type `Terminal`, press Enter

---

## Step 4 — Login to Docker Hub

```bash
docker login
```
Enter Docker Hub username and password when prompted.

> Don't have a Docker Hub account? Sign up free at [https://hub.docker.com](https://hub.docker.com)

---

## Step 5 — Pull the Images

```bash
docker pull ganeshkompella/privaterepo:backend
docker pull ganeshkompella/privaterepo:frontend
```

---

## Step 6 — Start the Backend

Replace `YOUR_GROQ_API_KEY` with the key you copied in Step 1.

**Windows (Command Prompt):**
```cmd
docker run -d --name ai-travel-backend -p 5000:5000 ^
  -e GROQ_API_KEY=YOUR_GROQ_API_KEY ^
  -e SECRET_KEY=travel-partner-secret-key-2026 ^
  -e JWT_SECRET=travel-jwt-secret-2026 ^
  ganeshkompella/privaterepo:backend
```

**Mac / Linux (Terminal):**
```bash
docker run -d --name ai-travel-backend -p 5000:5000 \
  -e GROQ_API_KEY=YOUR_GROQ_API_KEY \
  -e SECRET_KEY=travel-partner-secret-key-2026 \
  -e JWT_SECRET=travel-jwt-secret-2026 \
  ganeshkompella/privaterepo:backend
```

---

## Step 7 — Start the Frontend

```bash
docker run -d --name ai-travel-frontend -p 3000:80 ganeshkompella/privaterepo:frontend
```

---

## Step 8 — Open the App

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

## Stop / Start / Reset

```bash
# Stop containers
docker stop ai-travel-backend ai-travel-frontend

# Start again
docker start ai-travel-backend ai-travel-frontend

# Remove and start fresh
docker rm -f ai-travel-backend ai-travel-frontend
```
Then repeat Steps 6 and 7 to re-run.

---

## Run from Source Code

### Backend
```bash
cd backend
pip install -r requirements.txt
cp .env.example .env        # add your GROQ_API_KEY inside
python app.py
```

### Frontend
```bash
cd frontend
npm install --legacy-peer-deps
npm start
```

---

## Tech Stack

| Layer    | Technology                        |
|----------|-----------------------------------|
| Frontend | React 18, React Router, Axios     |
| Backend  | Flask, Flask-SQLAlchemy, PyJWT    |
| Database | SQLite                            |
| AI Model | Groq API — LLaMA 3.3 70B          |
| Auth     | JWT Tokens                        |
| Deploy   | Docker                            |
