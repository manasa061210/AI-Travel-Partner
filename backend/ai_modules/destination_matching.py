"""
Module 2: Content-Based Filtering for Destination Matching
Algorithm: Cosine Similarity on feature vectors
"""
import math


def _normalize(vec):
    """Normalize a vector to unit length."""
    magnitude = math.sqrt(sum(v ** 2 for v in vec))
    if magnitude == 0:
        return vec
    return [v / magnitude for v in vec]


def _cosine_similarity(vec_a, vec_b):
    """Compute cosine similarity between two vectors."""
    dot = sum(a * b for a, b in zip(vec_a, vec_b))
    return dot  # already normalized


CATEGORIES = ['beach', 'mountain', 'adventure', 'cultural', 'relaxation', 'city', 'wildlife', 'spiritual']
SEASONS = ['winter', 'summer', 'monsoon', 'spring', 'autumn']

SEASON_MAP = {
    'November to February': 'winter',
    'October to March': 'winter',
    'October to June': 'winter',
    'April to June': 'summer',
    'June to September': 'monsoon',
    'February to May': 'spring',
    'September to November': 'autumn',
}


def _dest_to_vector(destination):
    """Convert destination dict to a feature vector."""
    vec = []
    # Category one-hot (8 dims)
    for cat in CATEGORIES:
        vec.append(1.0 if destination.get('category', '') == cat else 0.0)
    # Normalized cost (inverse - cheaper = higher score baseline)
    cost = destination.get('base_cost_per_day', 3000)
    vec.append(1.0 - min(cost / 6000, 1.0))
    # Rating (normalized 0-1)
    vec.append((destination.get('rating', 3.0) - 1.0) / 4.0)
    # Season (simplified: always include, adjust per user)
    vec.append(0.5)
    return _normalize(vec)


def _pref_to_vector(preferences):
    """Convert user preferences to a feature vector."""
    interests = preferences.get('interests', [])
    budget = preferences.get('budget', 5000)
    vec = []
    # Category interests
    for cat in CATEGORIES:
        vec.append(1.0 if cat in interests else 0.0)
    # Budget preference
    vec.append(1.0 - min(budget / 6000, 1.0))
    # Prefer high-rated places
    vec.append(0.8)
    # Season match (neutral)
    vec.append(0.5)
    return _normalize(vec)


def match_destinations(preferences, destinations, top_n=6):
    """
    Match destinations to user preferences using content-based filtering.
    Returns top_n destinations sorted by similarity score.
    """
    if not destinations:
        return []

    pref_vec = _pref_to_vector(preferences)
    scored = []

    for dest in destinations:
        dest_vec = _dest_to_vector(dest)
        similarity = _cosine_similarity(pref_vec, dest_vec)

        # Bonus for exact interest match
        interests = preferences.get('interests', [])
        if dest.get('category') in interests:
            similarity = min(similarity + 0.15, 1.0)

        # Budget penalty: if destination is significantly over budget
        per_day_budget = preferences.get('budget', 99999) / max(preferences.get('days', 3), 1)
        if dest.get('base_cost_per_day', 0) > per_day_budget * 1.3:
            similarity *= 0.75

        scored.append({**dest, 'match_score': round(similarity, 3)})

    scored.sort(key=lambda x: x['match_score'], reverse=True)
    return scored[:top_n]
