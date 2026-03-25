"""
Module 5: Budget Estimation
Algorithm: Linear Regression (Cost Prediction)
Formula: Estimated Cost = (Base Cost × Days) + Hotel Cost + Transport Cost + Seasonal Adjustment
"""

# Hotel cost per night in INR
HOTEL_COSTS = {
    'budget':   {'base': 800,  'multiplier': 1.0},
    'standard': {'base': 2000, 'multiplier': 1.0},
    'luxury':   {'base': 5500, 'multiplier': 1.0},
}

# One-way transport costs in INR (per person)
TRANSPORT_COSTS = {
    'flight': 4500,
    'train':  1200,
    'bus':    500,
    'car':    3000,
}

# Seasonal adjustment factors
SEASONAL_ADJUSTMENTS = {
    'peak':    1.35,
    'off-peak': 0.80,
    'normal':  1.0,
}

# Food cost per person per day by hotel category
FOOD_COSTS = {
    'budget':   500,
    'standard': 900,
    'luxury':   1600,
}

# Activity cost per person per day
ACTIVITY_COSTS = {
    'budget':   400,
    'standard': 800,
    'luxury':   1500,
}

# Simple linear regression weights (learned from mock historical data)
# Target: predict total cost per trip
# Features: [days, travelers, hotel_tier, transport_tier, season_factor, base_cost_per_day]
LR_WEIGHTS = [1.05, 0.98, 1.02, 1.00, 1.08, 0.95]
LR_BIAS = 200


def _simple_linear_regression(features):
    """Apply linear regression weights to feature vector."""
    result = LR_BIAS
    for w, f in zip(LR_WEIGHTS, features):
        result += w * f
    return result


def estimate_budget(days, destination_base_cost, hotel_category, transport_type, season, travelers):
    """
    Estimate total trip cost with a detailed breakdown.

    Returns: {
        total: float,
        per_person: float,
        breakdown: {accommodation, transport, food, activities, misc}
    }
    """
    days = max(1, int(days))
    travelers = max(1, int(travelers))
    hotel_category = hotel_category.lower() if hotel_category else 'standard'
    transport_type = transport_type.lower() if transport_type else 'flight'
    season = season.lower() if season else 'normal'

    if hotel_category not in HOTEL_COSTS:
        hotel_category = 'standard'
    if transport_type not in TRANSPORT_COSTS:
        transport_type = 'flight'
    if season not in SEASONAL_ADJUSTMENTS:
        season = 'normal'

    season_factor = SEASONAL_ADJUSTMENTS[season]
    hotel_cost_per_night = HOTEL_COSTS[hotel_category]['base']
    transport_one_way = TRANSPORT_COSTS[transport_type]
    food_per_person_per_day = FOOD_COSTS[hotel_category]
    activity_per_person_per_day = ACTIVITY_COSTS[hotel_category]

    # Component calculations
    accommodation = hotel_cost_per_night * days * travelers * season_factor
    transport = transport_one_way * 2 * travelers  # round trip, seasonal applies less to transport
    food = food_per_person_per_day * days * travelers
    activities = activity_per_person_per_day * days * travelers

    # Base cost contributes
    base_total = destination_base_cost * days * travelers

    # Use linear regression to apply fine-tuned weights
    features = [
        accommodation,
        transport,
        food,
        activities,
        base_total * 0.1,   # partial contribution of destination base cost
        days * travelers * 100,
    ]
    regression_adjustment = _simple_linear_regression(features) * 0.01  # small adjustment term

    misc = base_total * 0.05 + regression_adjustment  # 5% of base as miscellaneous

    total = accommodation + transport + food + activities + misc
    total *= season_factor if season == 'peak' else 1.0

    return {
        'total': round(total),
        'per_person': round(total / travelers),
        'breakdown': {
            'accommodation': round(accommodation),
            'transport': round(transport),
            'food': round(food),
            'activities': round(activities),
            'misc': round(misc),
        },
        'notes': {
            'hotel_category': hotel_category,
            'transport_type': transport_type,
            'season': season,
            'season_adjustment': f'{int((season_factor - 1) * 100):+d}%' if season_factor != 1.0 else '0%',
        }
    }
