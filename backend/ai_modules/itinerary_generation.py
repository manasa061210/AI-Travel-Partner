"""
Module 4: Itinerary Generation
Algorithm: Greedy Scheduling — assign highest-rated available activities to time slots per day
"""
import json
from ai_modules.route_optimization import optimize_route

TIME_SLOTS = ['morning', 'afternoon', 'evening']

MEAL_SUGGESTIONS = {
    'beach':      {'breakfast': 'Fresh fruit bowl & coconut water at the shack', 'lunch': 'Seafood thali at a beachside restaurant', 'dinner': 'Candlelit dinner with grilled lobster'},
    'mountain':   {'breakfast': 'Parathas with local butter & hot chai', 'lunch': 'Maggi noodles and pakoras at a mountain café', 'dinner': 'Rajma-chawal or trout curry at the hotel'},
    'cultural':   {'breakfast': 'Poha/Jalebi at a local sweet shop', 'lunch': 'Thali at a heritage restaurant', 'dinner': 'Laal maas or regional specialty at a rooftop eatery'},
    'relaxation': {'breakfast': 'Idli-sambar and filter coffee', 'lunch': 'Sadya (banana leaf meal) or fish curry', 'dinner': 'Kerala prawns or vegetarian Ayurvedic dinner'},
    'adventure':  {'breakfast': 'Banana pancakes & energy bars', 'lunch': 'Quick bites at base camp café', 'dinner': 'Bonfire dinner with local daal-rice'},
    'city':       {'breakfast': 'Vada pav / pav bhaji at a street stall', 'lunch': 'Biriyani at a popular dhaba', 'dinner': 'Fine dining or rooftop restaurant'},
    'default':    {'breakfast': 'Local breakfast speciality', 'lunch': 'Regional thali', 'dinner': 'Popular local cuisine'},
}

HOTEL_SUGGESTIONS = {
    'budget':   ['Budget guest house / hostel', 'OYO or budget hotel', 'Dharamshala / home stay'],
    'standard': ['3-star hotel', 'Boutique hotel', 'Premium home stay'],
    'luxury':   ['5-star resort', 'Heritage palace hotel', 'Luxury villa'],
}

ACTIVITY_TEMPLATES = {
    'morning':   ['Visit {} and explore the surroundings', 'Morning guided tour of {}', 'Sunrise view from {}', 'Early morning walk through {}'],
    'afternoon': ['Explore {} in detail', 'Photography session at {}', 'Interactive tour at {}', 'Local experience near {}'],
    'evening':   ['Evening stroll around {}', 'Sunset view from {}', 'Night market / bazaar near {}', 'Cultural show at {}'],
}


def _get_category(destination_name, db_category=None):
    """Infer category from name or use provided."""
    if db_category:
        return db_category
    name_lower = destination_name.lower()
    if any(w in name_lower for w in ['goa', 'andaman', 'kovalam']):
        return 'beach'
    if any(w in name_lower for w in ['manali', 'ooty', 'coorg', 'munnar']):
        return 'mountain'
    if any(w in name_lower for w in ['jaipur', 'agra', 'varanasi', 'delhi']):
        return 'cultural'
    if any(w in name_lower for w in ['kerala', 'alleppey']):
        return 'relaxation'
    if any(w in name_lower for w in ['rishikesh']):
        return 'adventure'
    return 'city'


def generate_itinerary(destination, days, interests, budget, travelers,
                       hotel_category='standard', start_date=None, attractions=None, dest_category=None):
    """
    Greedy Scheduling Algorithm for itinerary generation.

    Selects highest-rated attractions and assigns them to time slots greedily.
    Returns day-by-day plan with activities, meals, accommodation.
    """
    days = max(1, int(days))
    travelers = max(1, int(travelers))
    category = dest_category or _get_category(destination)
    meal_set = MEAL_SUGGESTIONS.get(category, MEAL_SUGGESTIONS['default'])
    hotels = HOTEL_SUGGESTIONS.get(hotel_category, HOTEL_SUGGESTIONS['standard'])

    # Build attraction pool
    if not attractions:
        # Fallback attractions if none provided
        attractions = [
            {'name': f'{destination} Main Attraction', 'rating': 4.5, 'duration_hrs': 3, 'type': 'sightseeing', 'lat': 0, 'lng': 0},
            {'name': f'{destination} Historical Site', 'rating': 4.3, 'duration_hrs': 2, 'type': 'heritage', 'lat': 0, 'lng': 0},
            {'name': f'{destination} Local Market', 'rating': 4.1, 'duration_hrs': 2, 'type': 'shopping', 'lat': 0, 'lng': 0},
            {'name': f'{destination} Viewpoint', 'rating': 4.4, 'duration_hrs': 1.5, 'type': 'scenic', 'lat': 0, 'lng': 0},
            {'name': f'{destination} Cultural Centre', 'rating': 4.2, 'duration_hrs': 2, 'type': 'cultural', 'lat': 0, 'lng': 0},
            {'name': f'{destination} Nature Spot', 'rating': 4.6, 'duration_hrs': 3, 'type': 'nature', 'lat': 0, 'lng': 0},
        ]

    # --- Greedy Scheduling ---
    # Sort attractions by rating (desc) — greedy priority
    pool = sorted(attractions, key=lambda x: x.get('rating', 0), reverse=True)

    # Optimize route if coordinates are available
    places_with_coords = [a for a in pool if a.get('lat') and a.get('lng')]
    if len(places_with_coords) >= 2:
        route_result = optimize_route(places_with_coords)
        ordered_attractions = route_result['ordered_places']
        # Fill remaining without coords
        remaining = [a for a in pool if a not in ordered_attractions]
        ordered_attractions += remaining
    else:
        ordered_attractions = pool

    # Assign to slots: 3 slots per day (morning, afternoon, evening)
    total_slots = days * 3
    assigned = ordered_attractions[:total_slots]
    # Pad if fewer attractions
    while len(assigned) < total_slots:
        assigned.append({'name': f'Free time in {destination}', 'rating': 3.5, 'duration_hrs': 2, 'type': 'leisure'})

    plan_days = []
    slot_idx = 0

    for day_num in range(1, days + 1):
        day_activities = []
        slot_costs = {'morning': 300, 'afternoon': 400, 'evening': 200}

        for slot in TIME_SLOTS:
            attr = assigned[slot_idx] if slot_idx < len(assigned) else {'name': f'Free time in {destination}', 'duration_hrs': 2}
            slot_idx += 1

            # Pick activity description template
            template_list = ACTIVITY_TEMPLATES[slot]
            template = template_list[day_num % len(template_list)]

            day_activities.append({
                'time_slot': slot,
                'time': '08:00' if slot == 'morning' else ('13:00' if slot == 'afternoon' else '18:00'),
                'place': attr.get('name', 'Local attraction'),
                'activity': template.format(attr.get('name', 'the attraction')),
                'duration_hrs': attr.get('duration_hrs', 2),
                'type': attr.get('type', 'sightseeing'),
                'rating': attr.get('rating', 4.0),
                'estimated_cost': slot_costs[slot] * travelers,
            })

        # Daily cost estimate
        activity_cost = sum(a['estimated_cost'] for a in day_activities)
        from ai_modules.budget_estimation import FOOD_COSTS, HOTEL_COSTS, SEASONAL_ADJUSTMENTS
        food_cost = FOOD_COSTS.get(hotel_category, 900) * travelers
        hotel_cost = HOTEL_COSTS.get(hotel_category, {}).get('base', 2000)

        plan_days.append({
            'day': day_num,
            'date': _offset_date(start_date, day_num - 1),
            'activities': day_activities,
            'meals': {
                'breakfast': meal_set['breakfast'],
                'lunch': meal_set['lunch'],
                'dinner': meal_set['dinner'],
            },
            'accommodation': hotels[min(day_num - 1, len(hotels) - 1)],
            'day_cost': round(activity_cost + food_cost + (hotel_cost if day_num < days else 0)),
            'notes': f'Day {day_num} in {destination}. Enjoy and explore!',
        })

    # Transport day (day 1 arrival, last day departure)
    if plan_days:
        plan_days[0]['notes'] = f'Arrival day in {destination}. Check in and settle. Light exploration in the evening.'
        plan_days[-1]['notes'] = f'Last day in {destination}. Morning exploration, then departure.'

    total_cost = sum(d['day_cost'] for d in plan_days)

    return {
        'destination': destination,
        'days': days,
        'travelers': travelers,
        'category': category,
        'days_plan': plan_days,
        'total_cost': round(total_cost),
        'highlights': [a.get('name') for a in ordered_attractions[:5]],
        'tips': [
            f'Best time to visit {destination}: check weather forecast before travel.',
            'Carry sufficient cash as ATMs may be limited in remote areas.',
            'Respect local customs and dress codes at religious sites.',
            'Book accommodations in advance during peak season.',
        ]
    }


def _offset_date(start_date, offset_days):
    """Return a date string offset by given days from start_date."""
    if not start_date:
        return f'Day {offset_days + 1}'
    try:
        from datetime import datetime, timedelta
        dt = datetime.strptime(start_date, '%Y-%m-%d')
        return (dt + timedelta(days=offset_days)).strftime('%d %b %Y')
    except Exception:
        return start_date
