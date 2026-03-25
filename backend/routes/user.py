from flask import Blueprint, request, jsonify
from database import db
from models.user import User
from models.itinerary import Itinerary
from utils import token_required
import json

user_bp = Blueprint('user', __name__)


@user_bp.route('/profile', methods=['GET'])
@token_required
def get_profile(current_user):
    return jsonify({'success': True, 'data': current_user.to_dict()})


@user_bp.route('/profile', methods=['PUT'])
@token_required
def update_profile(current_user):
    data = request.get_json()
    if 'name' in data:
        current_user.name = data['name'].strip()
    if 'preferences' in data:
        current_user.preferences = json.dumps(data['preferences'])
    if 'password' in data and data['password']:
        if len(data['password']) < 6:
            return jsonify({'success': False, 'message': 'Password must be at least 6 characters'}), 400
        current_user.set_password(data['password'])
    db.session.commit()
    return jsonify({'success': True, 'message': 'Profile updated', 'data': current_user.to_dict()})


@user_bp.route('/trips', methods=['GET'])
@token_required
def get_trips(current_user):
    trips = Itinerary.query.filter_by(user_id=current_user.id).order_by(Itinerary.created_at.desc()).all()
    return jsonify({'success': True, 'data': [t.to_dict() for t in trips]})


@user_bp.route('/trips', methods=['POST'])
@token_required
def save_trip(current_user):
    data = request.get_json()
    destination = data.get('destination', '').strip()
    if not destination:
        return jsonify({'success': False, 'message': 'Destination is required'}), 400

    trip = Itinerary(
        user_id=current_user.id,
        title=data.get('title', f'Trip to {destination}'),
        destination=destination,
        days=data.get('days', 3),
        budget=data.get('budget', 0),
        travelers=data.get('travelers', 1),
        start_date=data.get('start_date', ''),
        interests=json.dumps(data.get('interests', [])),
        plan=json.dumps(data.get('plan', {})),
        total_cost=data.get('total_cost', 0),
        hotel_category=data.get('hotel_category', 'standard'),
        transport_type=data.get('transport_type', 'flight'),
        status='planned',
    )
    db.session.add(trip)
    db.session.commit()
    return jsonify({'success': True, 'message': 'Trip saved', 'data': trip.to_dict()}), 201


@user_bp.route('/trips/<int:trip_id>', methods=['GET'])
@token_required
def get_trip(current_user, trip_id):
    trip = Itinerary.query.filter_by(id=trip_id, user_id=current_user.id).first()
    if not trip:
        return jsonify({'success': False, 'message': 'Trip not found'}), 404
    return jsonify({'success': True, 'data': trip.to_dict()})


@user_bp.route('/trips/<int:trip_id>', methods=['DELETE'])
@token_required
def delete_trip(current_user, trip_id):
    trip = Itinerary.query.filter_by(id=trip_id, user_id=current_user.id).first()
    if not trip:
        return jsonify({'success': False, 'message': 'Trip not found'}), 404
    db.session.delete(trip)
    db.session.commit()
    return jsonify({'success': True, 'message': 'Trip deleted'})
