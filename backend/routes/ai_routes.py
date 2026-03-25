from flask import Blueprint, request, jsonify
from utils import token_required
import json
import os
import requests as http_requests
import re

ai_bp = Blueprint('ai', __name__)

GROQ_API_KEY = os.environ.get('GROQ_API_KEY', '')
GROQ_URL = 'https://api.groq.com/openai/v1/chat/completions'
MODEL = 'llama-3.3-70b-versatile'


def ask_groq(prompt, system='You are a helpful travel assistant. Respond with valid JSON only.'):
    """Call Groq API directly via HTTP and return the text response."""
    headers = {
        'Authorization': f'Bearer {GROQ_API_KEY}',
        'Content-Type': 'application/json',
    }
    body = {
        'model': MODEL,
        'messages': [
            {'role': 'system', 'content': system},
            {'role': 'user', 'content': prompt},
        ],
        'temperature': 0.7,
        'max_tokens': 4096,
    }
    resp = http_requests.post(GROQ_URL, headers=headers, json=body, timeout=60)
    resp.raise_for_status()
    return resp.json()['choices'][0]['message']['content']


def parse_json_response(text):
    """Extract JSON from model response even if it has extra text."""
    try:
        return json.loads(text)
    except Exception:
        pass
    match = re.search(r'```(?:json)?\s*([\s\S]+?)```', text)
    if match:
        try:
            return json.loads(match.group(1))
        except Exception:
            pass
    match = re.search(r'\{[\s\S]+\}', text)
    if match:
        try:
            return json.loads(match.group(0))
        except Exception:
            pass
    return None


# ── GENERATE ITINERARY ──────────────────────────────────────────────────────

@ai_bp.route('/generate-itinerary', methods=['POST'])
@token_required
def gen_itinerary(current_user):
    data = request.get_json()
    destination = data.get('destination', '').strip()
    if not destination:
        return jsonify({'success': False, 'message': 'Destination is required'}), 400

    days = int(data.get('days', 3))
    travelers = int(data.get('travelers', 1))
    budget = float(data.get('budget', 10000))
    interests = data.get('interests', [])
    start_date = data.get('start_date', '')
    hotel_category = data.get('hotel_category', 'standard')
    transport_type = data.get('transport_type', 'flight')
    interests_str = ', '.join(interests) if interests else 'sightseeing, local food, culture'

    prompt = f"""Create a detailed {days}-day travel itinerary for {destination}, India.

Trip details:
- Travelers: {travelers}
- Total budget: Rs {int(budget)}
- Interests: {interests_str}
- Hotel category: {hotel_category}
- Transport: {transport_type}
- Start date: {start_date or 'flexible'}

Return ONLY a valid JSON object in this exact format:
{{
  "destination": "{destination}",
  "total_days": {days},
  "travelers": {travelers},
  "category": "beach",
  "highlights": ["highlight1", "highlight2", "highlight3"],
  "tips": ["tip1", "tip2", "tip3"],
  "days": [
    {{
      "day": 1,
      "date": "Day 1",
      "daily_cost": 3000,
      "activities": [
        {{
          "time": "09:00 AM",
          "emoji": "emoji here",
          "name": "Activity name",
          "description": "Brief description",
          "type": "sightseeing",
          "duration": "2 hours",
          "cost": 500
        }}
      ],
      "meals": {{
        "breakfast": "Breakfast place or dish",
        "lunch": "Lunch place or dish",
        "dinner": "Dinner place or dish"
      }},
      "accommodation": "Hotel name and type",
      "note": "Special tip for this day"
    }}
  ],
  "budget_estimate": {{
    "total": {int(budget)},
    "breakdown": {{
      "accommodation": 0,
      "food": 0,
      "transport": 0,
      "activities": 0
    }}
  }}
}}

Include 3-4 activities per day. Make it realistic and specific to {destination}."""

    try:
        raw = ask_groq(prompt)
        result = parse_json_response(raw)
        if not result:
            return jsonify({'success': False, 'message': 'AI failed to generate itinerary. Try again.'}), 500
        return jsonify({'success': True, 'data': result})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500


# ── RECOMMEND DESTINATIONS ──────────────────────────────────────────────────

@ai_bp.route('/recommend-destinations', methods=['POST'])
@token_required
def recommend(current_user):
    data = request.get_json()
    budget = float(data.get('budget', 15000))
    interests = data.get('interests', [])
    duration = int(data.get('duration', 3))
    travelers = int(data.get('travelers', 1))
    text_input = data.get('text', '')
    interests_str = ', '.join(interests) if interests else 'general travel'
    extra = f'User says: "{text_input}"' if text_input else ''

    prompt = f"""Recommend 6 Indian travel destinations for:
- Budget: Rs {int(budget)} total
- Duration: {duration} days
- Travelers: {travelers}
- Interests: {interests_str}
{extra}

Return ONLY valid JSON:
{{
  "ranked": [
    {{
      "name": "Destination Name",
      "state": "State",
      "category": "beach",
      "description": "Why this suits the traveler in 2 sentences",
      "estimated_cost": 8000,
      "best_season": "Oct-Mar",
      "score": 92,
      "highlights": ["highlight1", "highlight2"]
    }}
  ],
  "preferences_used": {{
    "budget": {int(budget)},
    "duration": {duration}
  }}
}}"""

    try:
        raw = ask_groq(prompt, 'You are an expert Indian travel advisor. Respond with valid JSON only.')
        result = parse_json_response(raw)
        if not result:
            return jsonify({'success': False, 'message': 'AI recommendation failed.'}), 500
        return jsonify({'success': True, 'data': result})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500


# ── ESTIMATE BUDGET ─────────────────────────────────────────────────────────

@ai_bp.route('/estimate-budget', methods=['POST'])
@token_required
def budget_est(current_user):
    data = request.get_json()
    days = int(data.get('days', 3))
    destination = data.get('destination', 'India')
    hotel_category = data.get('hotel_category', 'standard')
    transport_type = data.get('transport_type', 'flight')
    travelers = int(data.get('travelers', 1))

    prompt = f"""Estimate travel budget for:
- Destination: {destination}, India
- Duration: {days} days
- Travelers: {travelers}
- Hotel: {hotel_category}
- Transport: {transport_type}

Return ONLY valid JSON:
{{
  "total": 15000,
  "per_person": 15000,
  "breakdown": {{
    "accommodation": 5000,
    "food": 3000,
    "transport": 4000,
    "activities": 2000,
    "miscellaneous": 1000
  }},
  "tips": ["money saving tip 1", "money saving tip 2"]
}}"""

    try:
        raw = ask_groq(prompt, 'You are a travel budget expert for India. Respond with valid JSON only.')
        result = parse_json_response(raw)
        if not result:
            return jsonify({'success': False, 'message': 'Budget estimation failed.'}), 500
        return jsonify({'success': True, 'data': result})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500


# ── FOOD RECOMMENDATIONS ────────────────────────────────────────────────────

@ai_bp.route('/food-recommendations', methods=['POST'])
def food_recommend():
    data = request.get_json()
    destination = data.get('destination', '').strip()
    if not destination:
        return jsonify({'success': False, 'message': 'Destination is required'}), 400

    prompt = f"""List the top 6 must-try foods in {destination}, India.

Return ONLY valid JSON:
{{
  "destination": "{destination}",
  "foods": [
    {{
      "name": "Dish name",
      "type": "Breakfast",
      "emoji": "emoji",
      "description": "Description of the dish and where it is typically eaten",
      "price_range": "Rs 80-150",
      "must_try": true
    }}
  ]
}}

Include a mix of must-try and popular local dishes specific to {destination}."""

    try:
        raw = ask_groq(prompt, 'You are a food expert on Indian regional cuisine. Respond with valid JSON only.')
        result = parse_json_response(raw)
        if not result:
            return jsonify({'success': False, 'message': 'Food recommendations failed.'}), 500
        return jsonify({'success': True, 'data': result})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500


# ── COMPARE DESTINATIONS ────────────────────────────────────────────────────

@ai_bp.route('/compare-destinations', methods=['POST'])
@token_required
def compare_dests(current_user):
    data = request.get_json()
    destination_names = data.get('destinations', [])
    if len(destination_names) < 2:
        return jsonify({'success': False, 'message': 'Provide at least 2 destinations'}), 400

    dests_str = ' vs '.join(destination_names)
    prompt = f"""Compare these Indian travel destinations: {dests_str}

Return ONLY valid JSON:
{{
  "comparison": [
    {{
      "name": "Destination",
      "scores": {{
        "value_for_money": 85,
        "natural_beauty": 90,
        "food": 80,
        "adventure": 70,
        "culture": 75,
        "accessibility": 85
      }},
      "best_for": "Who this is best for",
      "avoid_if": "When to avoid",
      "estimated_budget_per_day": 2500
    }}
  ],
  "verdict": "One sentence recommendation on which to pick and why"
}}"""

    try:
        raw = ask_groq(prompt, 'You are an Indian travel expert. Respond with valid JSON only.')
        result = parse_json_response(raw)
        if not result:
            return jsonify({'success': False, 'message': 'Comparison failed.'}), 500
        return jsonify({'success': True, 'data': result})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500
