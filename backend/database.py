from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash
import json

db = SQLAlchemy()

DESTINATIONS_SEED = [
    {
        "name": "Goa", "country": "India", "city": "Panaji",
        "category": "beach", "rating": 4.7, "base_cost_per_day": 3000,
        "description": "Sun, sand & vibrant nightlife on India's most beloved coastline. Perfect for beach lovers with golden shores, water sports and seafood delights.",
        "image_url": "", "best_season": "November to February",
        "weather_info": "Tropical climate, warm and humid. Avoid monsoon (June-Sept).",
        "popular_attractions": json.dumps([
            {"name": "Baga Beach", "lat": 15.5566, "lng": 73.7521, "type": "beach", "rating": 4.5, "duration_hrs": 3},
            {"name": "Calangute Beach", "lat": 15.5440, "lng": 73.7552, "type": "beach", "rating": 4.4, "duration_hrs": 2},
            {"name": "Fort Aguada", "lat": 15.4941, "lng": 73.7735, "type": "heritage", "rating": 4.3, "duration_hrs": 2},
            {"name": "Dudhsagar Falls", "lat": 15.3140, "lng": 74.3147, "type": "nature", "rating": 4.8, "duration_hrs": 4},
            {"name": "Old Goa Churches", "lat": 15.5009, "lng": 73.9116, "type": "cultural", "rating": 4.6, "duration_hrs": 3},
            {"name": "Anjuna Flea Market", "lat": 15.5742, "lng": 73.7404, "type": "shopping", "rating": 4.2, "duration_hrs": 2},
        ])
    },
    {
        "name": "Manali", "country": "India", "city": "Manali",
        "category": "mountain", "rating": 4.8, "base_cost_per_day": 2500,
        "description": "Snow-capped peaks, lush valleys and thrilling adventures await in the Himalayas. A paradise for trekkers, adventure seekers and nature lovers.",
        "image_url": "", "best_season": "October to June",
        "weather_info": "Cold mountain climate. Snowfall from Dec-Feb. Pleasant summers.",
        "popular_attractions": json.dumps([
            {"name": "Rohtang Pass", "lat": 32.3714, "lng": 77.2429, "type": "scenic", "rating": 4.8, "duration_hrs": 6},
            {"name": "Solang Valley", "lat": 32.3193, "lng": 77.1567, "type": "adventure", "rating": 4.7, "duration_hrs": 4},
            {"name": "Hadimba Temple", "lat": 32.2396, "lng": 77.1867, "type": "religious", "rating": 4.5, "duration_hrs": 2},
            {"name": "Old Manali", "lat": 32.2527, "lng": 77.1819, "type": "cultural", "rating": 4.4, "duration_hrs": 3},
            {"name": "Beas River Rafting", "lat": 32.2000, "lng": 77.1900, "type": "adventure", "rating": 4.6, "duration_hrs": 3},
            {"name": "Naggar Castle", "lat": 32.1001, "lng": 77.1668, "type": "heritage", "rating": 4.3, "duration_hrs": 2},
        ])
    },
    {
        "name": "Jaipur", "country": "India", "city": "Jaipur",
        "category": "cultural", "rating": 4.6, "base_cost_per_day": 2800,
        "description": "The Pink City, home to majestic forts, palaces and royal Rajasthani heritage. A feast for history lovers and architecture enthusiasts.",
        "image_url": "", "best_season": "October to March",
        "weather_info": "Semi-arid. Hot summers, pleasant winters. Avoid peak summer.",
        "popular_attractions": json.dumps([
            {"name": "Amber Fort", "lat": 26.9855, "lng": 75.8513, "type": "heritage", "rating": 4.8, "duration_hrs": 4},
            {"name": "City Palace", "lat": 26.9255, "lng": 75.8237, "type": "heritage", "rating": 4.7, "duration_hrs": 3},
            {"name": "Hawa Mahal", "lat": 26.9239, "lng": 75.8267, "type": "heritage", "rating": 4.6, "duration_hrs": 2},
            {"name": "Jantar Mantar", "lat": 26.9246, "lng": 75.8242, "type": "heritage", "rating": 4.5, "duration_hrs": 2},
            {"name": "Nahargarh Fort", "lat": 26.9480, "lng": 75.8068, "type": "heritage", "rating": 4.4, "duration_hrs": 3},
            {"name": "Johari Bazaar", "lat": 26.9196, "lng": 75.8267, "type": "shopping", "rating": 4.3, "duration_hrs": 2},
        ])
    },
    {
        "name": "Kerala", "country": "India", "city": "Kochi",
        "category": "relaxation", "rating": 4.9, "base_cost_per_day": 3200,
        "description": "God's Own Country — serene backwaters, houseboats, Ayurvedic retreats and lush greenery. The ultimate relaxation destination.",
        "image_url": "", "best_season": "September to March",
        "weather_info": "Tropical. Two monsoon seasons. Very pleasant post-monsoon.",
        "popular_attractions": json.dumps([
            {"name": "Alleppey Backwaters", "lat": 9.4981, "lng": 76.3388, "type": "nature", "rating": 4.9, "duration_hrs": 8},
            {"name": "Munnar Tea Gardens", "lat": 10.0892, "lng": 77.0595, "type": "nature", "rating": 4.8, "duration_hrs": 5},
            {"name": "Periyar Wildlife Sanctuary", "lat": 9.4738, "lng": 77.2063, "type": "wildlife", "rating": 4.7, "duration_hrs": 6},
            {"name": "Fort Kochi", "lat": 9.9666, "lng": 76.2425, "type": "heritage", "rating": 4.6, "duration_hrs": 3},
            {"name": "Kovalam Beach", "lat": 8.4004, "lng": 76.9784, "type": "beach", "rating": 4.5, "duration_hrs": 3},
            {"name": "Kathakali Show", "lat": 10.0158, "lng": 76.3419, "type": "cultural", "rating": 4.7, "duration_hrs": 2},
        ])
    },
    {
        "name": "Rishikesh", "country": "India", "city": "Rishikesh",
        "category": "adventure", "rating": 4.7, "base_cost_per_day": 2000,
        "description": "The Yoga Capital of the World with thrilling white-water rafting, bungee jumping, and deep spiritual energy on the banks of the Ganges.",
        "image_url": "", "best_season": "February to May, September to November",
        "weather_info": "Pleasant year-round except summer peak. Best for rafting Feb-May.",
        "popular_attractions": json.dumps([
            {"name": "Laxman Jhula", "lat": 30.1270, "lng": 78.3271, "type": "religious", "rating": 4.6, "duration_hrs": 2},
            {"name": "River Rafting", "lat": 30.1100, "lng": 78.3200, "type": "adventure", "rating": 4.9, "duration_hrs": 5},
            {"name": "Triveni Ghat", "lat": 30.1068, "lng": 78.3028, "type": "religious", "rating": 4.7, "duration_hrs": 2},
            {"name": "Neelkanth Mahadev", "lat": 30.2133, "lng": 78.3985, "type": "religious", "rating": 4.6, "duration_hrs": 3},
            {"name": "Beatles Ashram", "lat": 30.1190, "lng": 78.3296, "type": "cultural", "rating": 4.4, "duration_hrs": 2},
            {"name": "Bungee Jumping", "lat": 30.0977, "lng": 78.3300, "type": "adventure", "rating": 4.8, "duration_hrs": 2},
        ])
    },
    {
        "name": "Andaman Islands", "country": "India", "city": "Port Blair",
        "category": "beach", "rating": 4.8, "base_cost_per_day": 4500,
        "description": "Crystal-clear waters, coral reefs, pristine white beaches and lush tropical forests. An untouched paradise far from the mainland.",
        "image_url": "", "best_season": "November to May",
        "weather_info": "Tropical. Avoid monsoon (May-October). Perfect Nov-April.",
        "popular_attractions": json.dumps([
            {"name": "Radhanagar Beach", "lat": 11.9780, "lng": 92.9497, "type": "beach", "rating": 4.9, "duration_hrs": 4},
            {"name": "Cellular Jail", "lat": 11.6665, "lng": 92.7464, "type": "heritage", "rating": 4.7, "duration_hrs": 3},
            {"name": "Elephant Beach", "lat": 12.0155, "lng": 92.9797, "type": "beach", "rating": 4.8, "duration_hrs": 4},
            {"name": "Ross Island", "lat": 11.6792, "lng": 92.7732, "type": "heritage", "rating": 4.5, "duration_hrs": 3},
            {"name": "Scuba Diving", "lat": 11.9750, "lng": 92.9500, "type": "adventure", "rating": 4.9, "duration_hrs": 4},
            {"name": "Neil Island", "lat": 11.8338, "lng": 93.0436, "type": "beach", "rating": 4.7, "duration_hrs": 6},
        ])
    },
    {
        "name": "Varanasi", "country": "India", "city": "Varanasi",
        "category": "cultural", "rating": 4.5, "base_cost_per_day": 1800,
        "description": "One of the world's oldest living cities. Witness the mystical Ganga Aarti, ancient ghats and the spiritual soul of India.",
        "image_url": "", "best_season": "October to March",
        "weather_info": "Hot summers, cold winters. Best Oct-March for comfort.",
        "popular_attractions": json.dumps([
            {"name": "Dashashwamedh Ghat", "lat": 25.3068, "lng": 83.0116, "type": "religious", "rating": 4.9, "duration_hrs": 3},
            {"name": "Kashi Vishwanath Temple", "lat": 25.3109, "lng": 83.0107, "type": "religious", "rating": 4.8, "duration_hrs": 2},
            {"name": "Manikarnika Ghat", "lat": 25.3105, "lng": 83.0094, "type": "religious", "rating": 4.5, "duration_hrs": 2},
            {"name": "Sarnath", "lat": 25.3793, "lng": 83.0237, "type": "heritage", "rating": 4.7, "duration_hrs": 4},
            {"name": "Boat Ride on Ganges", "lat": 25.3067, "lng": 83.0100, "type": "scenic", "rating": 4.8, "duration_hrs": 2},
            {"name": "Banaras Silk Market", "lat": 25.3218, "lng": 83.0056, "type": "shopping", "rating": 4.3, "duration_hrs": 2},
        ])
    },
    {
        "name": "Agra", "country": "India", "city": "Agra",
        "category": "cultural", "rating": 4.6, "base_cost_per_day": 2500,
        "description": "Home to the iconic Taj Mahal, one of the Seven Wonders of the World. A city steeped in Mughal history, art and architecture.",
        "image_url": "", "best_season": "October to March",
        "weather_info": "Hot summers. Very cold winters. Best Oct-March.",
        "popular_attractions": json.dumps([
            {"name": "Taj Mahal", "lat": 27.1751, "lng": 78.0421, "type": "heritage", "rating": 5.0, "duration_hrs": 4},
            {"name": "Agra Fort", "lat": 27.1800, "lng": 78.0220, "type": "heritage", "rating": 4.7, "duration_hrs": 3},
            {"name": "Fatehpur Sikri", "lat": 27.0945, "lng": 77.6618, "type": "heritage", "rating": 4.6, "duration_hrs": 4},
            {"name": "Mehtab Bagh", "lat": 27.1820, "lng": 78.0290, "type": "scenic", "rating": 4.5, "duration_hrs": 2},
            {"name": "Itimad-ud-Daula", "lat": 27.1949, "lng": 78.0370, "type": "heritage", "rating": 4.4, "duration_hrs": 2},
            {"name": "Kinari Bazaar", "lat": 27.1807, "lng": 78.0077, "type": "shopping", "rating": 4.2, "duration_hrs": 2},
        ])
    },
    {
        "name": "Mumbai", "country": "India", "city": "Mumbai",
        "category": "city", "rating": 4.5, "base_cost_per_day": 4000,
        "description": "The City of Dreams — Bollywood, street food, colonial architecture and vibrant nightlife. India's financial capital never sleeps.",
        "image_url": "", "best_season": "November to February",
        "weather_info": "Tropical coastal. Avoid heavy monsoon (June-Sept). Pleasant winters.",
        "popular_attractions": json.dumps([
            {"name": "Gateway of India", "lat": 18.9220, "lng": 72.8347, "type": "heritage", "rating": 4.6, "duration_hrs": 2},
            {"name": "Marine Drive", "lat": 18.9442, "lng": 72.8237, "type": "scenic", "rating": 4.7, "duration_hrs": 2},
            {"name": "Elephanta Caves", "lat": 18.9633, "lng": 72.9315, "type": "heritage", "rating": 4.5, "duration_hrs": 4},
            {"name": "Juhu Beach", "lat": 19.0883, "lng": 72.8264, "type": "beach", "rating": 4.3, "duration_hrs": 2},
            {"name": "Chhatrapati Shivaji Terminus", "lat": 18.9401, "lng": 72.8354, "type": "heritage", "rating": 4.6, "duration_hrs": 1},
            {"name": "Dharavi Slum Tour", "lat": 19.0412, "lng": 72.8544, "type": "cultural", "rating": 4.4, "duration_hrs": 3},
        ])
    },
    {
        "name": "Coorg", "country": "India", "city": "Madikeri",
        "category": "relaxation", "rating": 4.7, "base_cost_per_day": 3000,
        "description": "Scotland of India — rolling coffee plantations, misty hills, cascading waterfalls and fresh mountain air. Perfect for a serene retreat.",
        "image_url": "", "best_season": "October to May",
        "weather_info": "Cool and pleasant. Rainfall year-round but manageable Oct-May.",
        "popular_attractions": json.dumps([
            {"name": "Abbey Falls", "lat": 12.4200, "lng": 75.7260, "type": "nature", "rating": 4.6, "duration_hrs": 2},
            {"name": "Raja's Seat", "lat": 12.4253, "lng": 75.7374, "type": "scenic", "rating": 4.5, "duration_hrs": 1},
            {"name": "Nagarhole National Park", "lat": 12.0534, "lng": 76.1100, "type": "wildlife", "rating": 4.7, "duration_hrs": 5},
            {"name": "Dubare Elephant Camp", "lat": 12.3575, "lng": 75.8867, "type": "wildlife", "rating": 4.6, "duration_hrs": 3},
            {"name": "Talakaveri", "lat": 12.3872, "lng": 75.5018, "type": "religious", "rating": 4.4, "duration_hrs": 3},
            {"name": "Coffee Plantation Tour", "lat": 12.4200, "lng": 75.7400, "type": "cultural", "rating": 4.8, "duration_hrs": 3},
        ])
    },
    {
        "name": "Ooty", "country": "India", "city": "Ooty",
        "category": "mountain", "rating": 4.5, "base_cost_per_day": 2200,
        "description": "Queen of Hill Stations — lush tea gardens, a scenic toy train ride, beautiful botanical gardens and cool misty mornings.",
        "image_url": "", "best_season": "April to June, September to November",
        "weather_info": "Cool and pleasant. Some rain in monsoon. Avoid Dec-Jan if sensitive to cold.",
        "popular_attractions": json.dumps([
            {"name": "Ooty Botanical Gardens", "lat": 11.4115, "lng": 76.6905, "type": "nature", "rating": 4.5, "duration_hrs": 3},
            {"name": "Nilgiri Mountain Railway", "lat": 11.4129, "lng": 76.6949, "type": "scenic", "rating": 4.8, "duration_hrs": 4},
            {"name": "Ooty Lake", "lat": 11.4011, "lng": 76.6933, "type": "scenic", "rating": 4.3, "duration_hrs": 2},
            {"name": "Doddabetta Peak", "lat": 11.3884, "lng": 76.7399, "type": "nature", "rating": 4.6, "duration_hrs": 3},
            {"name": "Rose Garden", "lat": 11.4178, "lng": 76.7059, "type": "nature", "rating": 4.4, "duration_hrs": 2},
            {"name": "Tea Factory", "lat": 11.4000, "lng": 76.7000, "type": "cultural", "rating": 4.5, "duration_hrs": 2},
        ])
    },
    {
        "name": "Delhi", "country": "India", "city": "New Delhi",
        "category": "city", "rating": 4.4, "base_cost_per_day": 3500,
        "description": "India's capital blends ancient history with modern buzz. From Mughal monuments to street food, it's a sensory overload in the best way.",
        "image_url": "", "best_season": "October to March",
        "weather_info": "Extreme summers and winters. October-March is ideal. Avoid May-June heat.",
        "popular_attractions": json.dumps([
            {"name": "Red Fort", "lat": 28.6562, "lng": 77.2410, "type": "heritage", "rating": 4.6, "duration_hrs": 3},
            {"name": "Qutub Minar", "lat": 28.5244, "lng": 77.1855, "type": "heritage", "rating": 4.7, "duration_hrs": 2},
            {"name": "India Gate", "lat": 28.6129, "lng": 77.2295, "type": "heritage", "rating": 4.5, "duration_hrs": 1},
            {"name": "Humayun's Tomb", "lat": 28.5933, "lng": 77.2507, "type": "heritage", "rating": 4.6, "duration_hrs": 2},
            {"name": "Chandni Chowk", "lat": 28.6507, "lng": 77.2309, "type": "cultural", "rating": 4.4, "duration_hrs": 3},
            {"name": "Lotus Temple", "lat": 28.5535, "lng": 77.2588, "type": "religious", "rating": 4.5, "duration_hrs": 2},
        ])
    },
]


def init_db(app):
    db.init_app(app)
    with app.app_context():
        db.create_all()
        _seed_data()


def _seed_data():
    from models.user import User
    from models.destination import Destination

    if User.query.count() == 0:
        admin = User(name='Admin', email='admin@travel.com', role='admin',
                     preferences=json.dumps({'interests': ['cultural', 'city'], 'budget_pref': 'standard'}))
        admin.set_password('admin123')

        demo = User(name='Rahul Sharma', email='user@travel.com', role='user',
                    preferences=json.dumps({'interests': ['adventure', 'mountain', 'beach'], 'budget_pref': 'standard'}))
        demo.set_password('user123')

        db.session.add_all([admin, demo])
        db.session.commit()

    if Destination.query.count() == 0:
        for d in DESTINATIONS_SEED:
            dest = Destination(**d)
            db.session.add(dest)
        db.session.commit()
