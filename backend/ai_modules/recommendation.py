"""
Module 6: Recommendation & Comparison
Algorithm: Multi-Criteria Decision Analysis (MCDA) with weighted scoring
"""

DEFAULT_WEIGHTS = {
    'cost':       0.30,
    'popularity': 0.20,
    'rating':     0.20,
    'safety':     0.10,
    'weather':    0.10,
    'interest':   0.10,
}

# Safety index by destination (0-10 scale, sourced from general knowledge)
SAFETY_INDEX = {
    'Goa': 7.5, 'Manali': 8.0, 'Jaipur': 7.8, 'Kerala': 8.5,
    'Rishikesh': 8.2, 'Andaman Islands': 8.8, 'Varanasi': 7.0,
    'Agra': 7.2, 'Mumbai': 7.5, 'Delhi': 6.8, 'Coorg': 8.5, 'Ooty': 8.3,
}

# Popularity index (0-10 scale)
POPULARITY_INDEX = {
    'Goa': 9.5, 'Manali': 9.0, 'Jaipur': 8.8, 'Kerala': 9.2,
    'Rishikesh': 8.5, 'Andaman Islands': 8.0, 'Varanasi': 8.3,
    'Agra': 9.0, 'Mumbai': 9.3, 'Delhi': 9.0, 'Coorg': 7.5, 'Ooty': 7.8,
}


def _normalize_scores(destinations, key):
    """Min-max normalization of a metric across destinations."""
    values = [d.get(key, 0) for d in destinations]
    min_val, max_val = min(values), max(values)
    if max_val == min_val:
        return [0.5] * len(destinations)
    return [(v - min_val) / (max_val - min_val) for v in values]


def rank_destinations(destinations, weights=None, user_interests=None, budget=None):
    """
    Rank destinations using Multi-Criteria Decision Analysis.

    Each criterion is normalized 0-1 then weighted and summed.
    Returns destinations sorted by final MCDA score.
    """
    if not destinations:
        return []

    w = {**DEFAULT_WEIGHTS, **(weights or {})}
    # Normalize weights to sum to 1
    total_w = sum(w.values())
    w = {k: v / total_w for k, v in w.items()}

    n = len(destinations)

    # --- Cost score (lower cost = higher score) ---
    costs = [d.get('base_cost_per_day', 3000) for d in destinations]
    min_c, max_c = min(costs), max(costs)
    cost_scores = [(max_c - c) / (max_c - min_c) if max_c != min_c else 0.5 for c in costs]

    # --- Popularity score ---
    pop_scores = [POPULARITY_INDEX.get(d.get('name', ''), 7.0) / 10.0 for d in destinations]

    # --- Rating score ---
    ratings = [d.get('rating', 4.0) for d in destinations]
    min_r, max_r = min(ratings), max(ratings)
    rating_scores = [(r - min_r) / (max_r - min_r) if max_r != min_r else 0.5 for r in ratings]

    # --- Safety score ---
    safety_scores = [SAFETY_INDEX.get(d.get('name', ''), 7.5) / 10.0 for d in destinations]

    # --- Weather/Season score (simplified: all score 0.7 unless we have more data) ---
    weather_scores = [0.7] * n

    # --- Interest match score ---
    if user_interests:
        interest_scores = [
            1.0 if d.get('category') in user_interests else 0.2
            for d in destinations
        ]
    else:
        interest_scores = [0.5] * n

    # --- Budget penalty ---
    if budget:
        days = 3  # default assumption
        for i, d in enumerate(destinations):
            if d.get('base_cost_per_day', 0) * days > budget:
                cost_scores[i] *= 0.6  # penalize over-budget

    # --- Final weighted MCDA score ---
    scored = []
    for i, dest in enumerate(destinations):
        score = (
            w['cost']       * cost_scores[i] +
            w['popularity'] * pop_scores[i] +
            w['rating']     * rating_scores[i] +
            w['safety']     * safety_scores[i] +
            w['weather']    * weather_scores[i] +
            w['interest']   * interest_scores[i]
        )
        scored.append({
            **dest,
            'mcda_score': round(score, 3),
            'score_breakdown': {
                'cost':       round(cost_scores[i], 3),
                'popularity': round(pop_scores[i], 3),
                'rating':     round(rating_scores[i], 3),
                'safety':     round(safety_scores[i], 3),
                'interest':   round(interest_scores[i], 3),
            }
        })

    scored.sort(key=lambda x: x['mcda_score'], reverse=True)
    return scored


def compare_destinations(destinations, criteria=None):
    """
    Build a comparison matrix for a set of destinations.
    Returns pairwise comparison data useful for displaying a comparison table.
    """
    if not destinations:
        return {'matrix': [], 'winner': None}

    ranked = rank_destinations(destinations, weights=criteria)

    comparison_table = []
    for dest in ranked:
        comparison_table.append({
            'name': dest.get('name'),
            'category': dest.get('category'),
            'cost_per_day': dest.get('base_cost_per_day'),
            'rating': dest.get('rating'),
            'safety': SAFETY_INDEX.get(dest.get('name', ''), 7.5),
            'popularity': POPULARITY_INDEX.get(dest.get('name', ''), 7.0),
            'best_season': dest.get('best_season', ''),
            'mcda_score': dest.get('mcda_score'),
            'score_breakdown': dest.get('score_breakdown', {}),
            'recommended': False,
        })

    if comparison_table:
        comparison_table[0]['recommended'] = True

    return {
        'matrix': comparison_table,
        'winner': comparison_table[0]['name'] if comparison_table else None,
        'weights_used': criteria or DEFAULT_WEIGHTS,
    }
