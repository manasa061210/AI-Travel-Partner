"""
Module 1: NLP-Based Travel Intent Extraction
Algorithm: Tokenization + Keyword Extraction + Category Classification
"""
import re

CATEGORY_KEYWORDS = {
    'beach':      ['beach', 'sea', 'ocean', 'coastal', 'island', 'shore', 'surf', 'snorkel', 'diving', 'coral', 'sunbath', 'sand'],
    'mountain':   ['mountain', 'hill', 'trek', 'hiking', 'peak', 'snow', 'himalaya', 'altitude', 'valley', 'glacier', 'camp'],
    'adventure':  ['adventure', 'rafting', 'bungee', 'paragliding', 'skydiving', 'climbing', 'zip', 'extreme', 'thrill', 'sport'],
    'cultural':   ['culture', 'heritage', 'history', 'museum', 'fort', 'palace', 'temple', 'monument', 'art', 'tradition', 'ancient'],
    'relaxation': ['relax', 'spa', 'yoga', 'meditation', 'peaceful', 'calm', 'quiet', 'retreat', 'wellness', 'ayurveda', 'backwater'],
    'city':       ['city', 'urban', 'shopping', 'nightlife', 'food', 'street', 'market', 'metro', 'modern', 'cosmopolitan'],
    'wildlife':   ['wildlife', 'safari', 'jungle', 'tiger', 'elephant', 'forest', 'national park', 'bird', 'nature'],
    'spiritual':  ['spiritual', 'pilgrimage', 'temple', 'shrine', 'holy', 'devotion', 'meditation', 'ganga', 'ghat', 'aarti'],
}

BUDGET_PATTERNS = [
    (r'₹\s*([\d,]+)', 'inr'),
    (r'rs\.?\s*([\d,]+)', 'inr'),
    (r'budget\s+of\s+([\d,]+)', 'inr'),
    (r'([\d,]+)\s+rupee', 'inr'),
    (r'under\s+([\d,]+)', 'inr'),
    (r'below\s+([\d,]+)', 'inr'),
]

DURATION_PATTERNS = [
    r'(\d+)\s*day',
    r'(\d+)\s*night',
    r'(\d+)\s*week',
    r'for\s+(\d+)',
]


def _tokenize(text):
    """Simple word tokenizer."""
    text = text.lower()
    text = re.sub(r'[^\w\s]', ' ', text)
    return text.split()


def extract_preferences(text):
    """
    Extract structured travel preferences from natural language input.
    Returns: {interests, travel_type, budget_hint, duration_hint, keywords}
    """
    if not text:
        return {'interests': [], 'travel_type': 'general', 'budget_hint': None, 'duration_hint': None, 'keywords': []}

    text_lower = text.lower()
    tokens = _tokenize(text)

    # --- Category / Interest Scoring ---
    scores = {}
    for category, keywords in CATEGORY_KEYWORDS.items():
        score = 0
        for kw in keywords:
            if kw in text_lower:
                score += 2 if ' ' not in kw else 3   # multi-word gets higher weight
            elif any(t.startswith(kw[:4]) for t in tokens if len(kw) > 4):
                score += 1
        scores[category] = score

    # Sort by score
    ranked = sorted(scores.items(), key=lambda x: x[1], reverse=True)
    interests = [cat for cat, score in ranked if score > 0]
    travel_type = ranked[0][0] if ranked[0][1] > 0 else 'general'

    # --- Budget Extraction ---
    budget_hint = None
    for pattern, currency in BUDGET_PATTERNS:
        match = re.search(pattern, text_lower)
        if match:
            raw = match.group(1).replace(',', '')
            try:
                budget_hint = float(raw)
                break
            except ValueError:
                pass

    # --- Duration Extraction ---
    duration_hint = None
    for pattern in DURATION_PATTERNS:
        match = re.search(pattern, text_lower)
        if match:
            val = int(match.group(1))
            if 'week' in pattern:
                val *= 7
            duration_hint = val
            break

    # Key extracted nouns (simple: tokens > 4 chars, not stop words)
    STOP_WORDS = {'want', 'need', 'like', 'would', 'going', 'travel', 'trip', 'plan', 'visit', 'place', 'there', 'with'}
    keywords = [t for t in tokens if len(t) > 4 and t not in STOP_WORDS][:10]

    return {
        'interests': interests[:5],
        'travel_type': travel_type,
        'budget_hint': budget_hint,
        'duration_hint': duration_hint,
        'keywords': keywords,
    }
