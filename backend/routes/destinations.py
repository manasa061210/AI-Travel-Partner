from flask import Blueprint, request, jsonify
from database import db
from models.destination import Destination, Review
from models.user import User
from utils import token_required
from datetime import datetime

destinations_bp = Blueprint('destinations', __name__)


@destinations_bp.route('/', methods=['GET'])
def list_destinations():
    search = request.args.get('search', '').strip()
    category = request.args.get('category', '').strip()
    budget_min = request.args.get('budget_min', type=float)
    budget_max = request.args.get('budget_max', type=float)

    query = Destination.query
    if search:
        query = query.filter(
            db.or_(
                Destination.name.ilike(f'%{search}%'),
                Destination.city.ilike(f'%{search}%'),
                Destination.country.ilike(f'%{search}%'),
                Destination.description.ilike(f'%{search}%'),
            )
        )
    if category:
        query = query.filter_by(category=category)
    if budget_min is not None:
        query = query.filter(Destination.base_cost_per_day >= budget_min)
    if budget_max is not None:
        query = query.filter(Destination.base_cost_per_day <= budget_max)

    destinations = query.order_by(Destination.rating.desc()).all()
    return jsonify({'success': True, 'data': [d.to_dict() for d in destinations]})


@destinations_bp.route('/<int:dest_id>', methods=['GET'])
def get_destination(dest_id):
    dest = Destination.query.get_or_404(dest_id)
    data = dest.to_dict()
    reviews = [r.to_dict() for r in dest.reviews]
    data['reviews'] = reviews
    return jsonify({'success': True, 'data': data})


@destinations_bp.route('/<int:dest_id>/review', methods=['POST'])
@token_required
def add_review(current_user, dest_id):
    dest = Destination.query.get_or_404(dest_id)
    data = request.get_json()
    rating = data.get('rating')
    comment = data.get('comment', '').strip()

    if rating is None or not (1 <= float(rating) <= 5):
        return jsonify({'success': False, 'message': 'Rating must be between 1 and 5'}), 400

    review = Review(
        destination_id=dest_id,
        user_id=current_user.id,
        rating=float(rating),
        comment=comment,
        created_at=datetime.utcnow(),
    )
    db.session.add(review)

    # Update destination average rating
    db.session.flush()
    all_ratings = [r.rating for r in dest.reviews]
    dest.rating = round(sum(all_ratings) / len(all_ratings), 1)
    db.session.commit()

    return jsonify({'success': True, 'message': 'Review added', 'data': review.to_dict()}), 201
