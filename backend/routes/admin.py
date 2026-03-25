from flask import Blueprint, request, jsonify
from database import db
from models.user import User
from models.destination import Destination, Review
from models.itinerary import Itinerary
from utils import admin_required
import json

admin_bp = Blueprint('admin', __name__)


@admin_bp.route('/stats', methods=['GET'])
@admin_required
def stats(current_user):
    user_count = User.query.filter_by(role='user').count()
    trip_count = Itinerary.query.count()
    dest_count = Destination.query.count()

    # Top destinations by trip count
    from sqlalchemy import func
    top_dests = db.session.query(
        Itinerary.destination,
        func.count(Itinerary.id).label('count')
    ).group_by(Itinerary.destination).order_by(func.count(Itinerary.id).desc()).limit(5).all()

    return jsonify({
        'success': True,
        'data': {
            'total_users': user_count,
            'total_trips': trip_count,
            'total_destinations': dest_count,
            'popular_destinations': [{'name': d, 'count': c} for d, c in top_dests],
        }
    })


@admin_bp.route('/users', methods=['GET'])
@admin_required
def list_users(current_user):
    users = User.query.order_by(User.created_at.desc()).all()
    return jsonify({'success': True, 'data': [u.to_dict() for u in users]})


@admin_bp.route('/users/<int:user_id>', methods=['DELETE'])
@admin_required
def delete_user(current_user, user_id):
    user = User.query.get_or_404(user_id)
    if user.role == 'admin':
        return jsonify({'success': False, 'message': 'Cannot delete admin user'}), 403
    db.session.delete(user)
    db.session.commit()
    return jsonify({'success': True, 'message': 'User deleted'})


@admin_bp.route('/destinations', methods=['POST'])
@admin_required
def create_destination(current_user):
    data = request.get_json()
    dest = Destination(
        name=data.get('name'),
        country=data.get('country', 'India'),
        city=data.get('city', ''),
        category=data.get('category', 'city'),
        description=data.get('description', ''),
        base_cost_per_day=data.get('base_cost_per_day', 2000),
        rating=data.get('rating', 4.0),
        popular_attractions=json.dumps(data.get('popular_attractions', [])),
        best_season=data.get('best_season', ''),
        weather_info=data.get('weather_info', ''),
    )
    db.session.add(dest)
    db.session.commit()
    return jsonify({'success': True, 'message': 'Destination created', 'data': dest.to_dict()}), 201


@admin_bp.route('/destinations/<int:dest_id>', methods=['PUT'])
@admin_required
def update_destination(current_user, dest_id):
    dest = Destination.query.get_or_404(dest_id)
    data = request.get_json()
    for field in ['name', 'country', 'city', 'category', 'description', 'best_season', 'weather_info']:
        if field in data:
            setattr(dest, field, data[field])
    if 'base_cost_per_day' in data:
        dest.base_cost_per_day = float(data['base_cost_per_day'])
    if 'rating' in data:
        dest.rating = float(data['rating'])
    if 'popular_attractions' in data:
        dest.popular_attractions = json.dumps(data['popular_attractions'])
    db.session.commit()
    return jsonify({'success': True, 'message': 'Destination updated', 'data': dest.to_dict()})


@admin_bp.route('/destinations/<int:dest_id>', methods=['DELETE'])
@admin_required
def delete_destination(current_user, dest_id):
    dest = Destination.query.get_or_404(dest_id)
    db.session.delete(dest)
    db.session.commit()
    return jsonify({'success': True, 'message': 'Destination deleted'})


@admin_bp.route('/reviews', methods=['GET'])
@admin_required
def list_reviews(current_user):
    reviews = Review.query.order_by(Review.created_at.desc()).all()
    return jsonify({'success': True, 'data': [r.to_dict() for r in reviews]})


@admin_bp.route('/reviews/<int:review_id>', methods=['DELETE'])
@admin_required
def delete_review(current_user, review_id):
    review = Review.query.get_or_404(review_id)
    db.session.delete(review)
    db.session.commit()
    return jsonify({'success': True, 'message': 'Review deleted'})
