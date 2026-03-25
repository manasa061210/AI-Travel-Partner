# AI Travel Partner — Pseudocode

This document explains the core logic of the AI Travel Partner application in simple pseudocode.

---

## 1. User Authentication

### Register
```
FUNCTION register(name, email, password):
    IF email already exists in database:
        RETURN error "Email already registered"

    hash = bcrypt(password)
    CREATE new User(name, email, hash)
    SAVE to database
    token = generate_jwt(user.id)
    RETURN token
```

### Login
```
FUNCTION login(email, password):
    user = FIND user by email in database
    IF user NOT found:
        RETURN error "Invalid credentials"

    IF bcrypt_check(password, user.hash) is FALSE:
        RETURN error "Invalid credentials"

    token = generate_jwt(user.id)
    RETURN token, user details
```

### Protected Route (JWT Middleware)
```
FUNCTION token_required(request):
    token = GET token from request header

    IF token is missing:
        RETURN error "Token missing"

    user_id = decode_jwt(token)
    IF decode fails:
        RETURN error "Invalid or expired token"

    current_user = FIND user by user_id
    PASS current_user to next function
```

---

## 2. AI Itinerary Generation

```
FUNCTION generate_itinerary(destination, days, travelers, budget, interests, hotel, transport):

    prompt = BUILD prompt with:
        - destination, days, travelers, budget
        - interests (e.g. adventure, food, culture)
        - hotel category (budget / standard / luxury)
        - transport type (flight / train / bus / car)

    response = CALL Groq AI API (LLaMA 3.3 70B) with prompt

    itinerary = PARSE JSON from response

    itinerary contains:
        FOR each day in days:
            - List of 3-4 activities (time, place, description, cost)
            - Meals (breakfast, lunch, dinner)
            - Accommodation details
            - Daily cost
        - Budget breakdown (accommodation, food, transport, activities)
        - Highlights and travel tips

    SAVE itinerary as trip in database
    RETURN itinerary
```

---

## 3. Destination Recommendations

```
FUNCTION recommend_destinations(budget, interests, duration, travelers):

    prompt = BUILD prompt with:
        - User budget, interests, trip duration, number of travelers

    response = CALL Groq AI API with prompt

    recommendations = PARSE JSON from response

    recommendations contains list of 6 destinations:
        FOR each destination:
            - Name, State, Category
            - Why it suits the traveler
            - Estimated cost
            - Best season to visit
            - Score (out of 100)
            - Key highlights

    RETURN recommendations sorted by score
```

---

## 4. Budget Estimation

```
FUNCTION estimate_budget(destination, days, travelers, hotel_category, transport_type):

    prompt = BUILD prompt with all trip details

    response = CALL Groq AI API with prompt

    budget = PARSE JSON from response

    budget contains:
        - total cost
        - cost per person
        - breakdown:
            accommodation = f(hotel_category, days, travelers)
            food          = f(destination, days, travelers)
            transport     = f(transport_type, destination)
            activities    = f(interests, days)
            miscellaneous = small buffer amount
        - money saving tips

    RETURN budget
```

---

## 5. Food Recommendations

```
FUNCTION food_recommendations(destination):

    IF destination is empty:
        RETURN error "Destination required"

    prompt = BUILD prompt asking for top 6 local foods in destination

    response = CALL Groq AI API with prompt

    foods = PARSE JSON from response

    foods contains list of dishes:
        FOR each dish:
            - Name and emoji
            - Type (Breakfast / Lunch / Dinner / Snack / Dessert)
            - Description and where to find it
            - Price range in Rupees
            - Whether it is a must-try

    RETURN food list
```

---

## 6. Trip Save and Retrieval

### Save Trip
```
FUNCTION save_trip(user, destination, days, travelers, plan, total_cost):

    CREATE new Trip:
        - user_id      = current user
        - destination  = destination
        - days         = days
        - travelers    = travelers
        - plan         = JSON.stringify(itinerary)
        - total_cost   = total_cost
        - status       = "planned"

    SAVE to database
    RETURN trip with id
```

### Get Trip
```
FUNCTION get_trip(trip_id, user):

    trip = FIND trip by id in database

    IF trip NOT found:
        RETURN error "Trip not found"

    IF trip.user_id != user.id:
        RETURN error "Unauthorized"

    plan = JSON.parse(trip.plan)
    RETURN trip details + plan
```

---

## 7. Frontend Flow

### Home Page
```
ON page load:
    SHOW gold title, search bar, destination cards

ON search input:
    FILTER destination cards by name

ON destination card click:
    NAVIGATE to Plan Trip page with destination pre-filled
```

### Plan Trip (3 Steps)
```
STEP 1 — Destination & Basics:
    User enters: destination, days, travelers, start date, budget
    ON Next:
        IF destination is empty → SHOW alert
        ELSE → GO to Step 2

STEP 2 — Preferences:
    User selects: interests, hotel category, transport, season
    CALL estimate_budget API → SHOW live budget estimate sidebar
    ON Generate:
        GO to Step 3

STEP 3 — Generating:
    CALL generate_itinerary API
    SHOW loading animation with messages
    ON success:
        SAVE trip to database
        NAVIGATE to Itinerary page
    ON failure:
        SHOW error message
        GO back to Step 2
```

### Itinerary Page
```
ON page load:
    FETCH trip by id from API
    PARSE plan JSON from trip

    DISPLAY:
        - Header: destination, date, travelers, total budget
        - Budget breakdown bars
        - Day-by-day plan:
            FOR each day:
                SHOW activities with time, emoji, name, cost
                SHOW meals (breakfast, lunch, dinner)
                SHOW accommodation
        - Travel tips
        - Highlights sidebar
        - Trip info sidebar
```

---

## 8. Admin Dashboard

```
FUNCTION get_stats():
    total_users        = COUNT all users
    total_trips        = COUNT all trips
    total_destinations = COUNT all destinations
    RETURN stats

FUNCTION manage_destinations():
    GET all destinations
    ALLOW admin to:
        - ADD new destination
        - EDIT existing destination
        - DELETE destination

FUNCTION manage_users():
    GET all users
    ALLOW admin to VIEW user list and roles
```

---

## 9. Overall System Flow

```
User opens app
    → Registers / Logs in  →  JWT token stored in browser

User on Home Page
    → Searches / clicks destination

User on Plan Trip
    → Fills in trip details
    → AI generates itinerary via Groq API
    → Trip saved to SQLite database
    → Redirected to Itinerary page

User on Itinerary Page
    → Views day-by-day plan, budget, tips

User on Food Page
    → Enters destination
    → AI returns local food recommendations

User on Dashboard
    → Views all saved trips
    → AI recommends new destinations based on profile

Admin
    → Manages destinations and users
```
