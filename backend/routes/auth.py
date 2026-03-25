from flask import Blueprint, request, jsonify
from database import db
from models.user import User
from utils import generate_token, token_required
import json

auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    name = data.get('name', '').strip()
    email = data.get('email', '').strip().lower()
    password = data.get('password', '')
    preferences = data.get('preferences', {})

    if not name or not email or not password:
        return jsonify({'success': False, 'message': 'Name, email and password are required'}), 400

    if len(password) < 6:
        return jsonify({'success': False, 'message': 'Password must be at least 6 characters'}), 400

    if User.query.filter_by(email=email).first():
        return jsonify({'success': False, 'message': 'Email already registered'}), 409

    user = User(name=name, email=email, role='user',
                preferences=json.dumps(preferences))
    user.set_password(password)
    db.session.add(user)
    db.session.commit()

    token = generate_token(user.id, user.role)
    return jsonify({
        'success': True,
        'message': 'Registration successful',
        'data': {'token': token, 'user': user.to_dict()}
    }), 201


@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email', '').strip().lower()
    password = data.get('password', '')

    if not email or not password:
        return jsonify({'success': False, 'message': 'Email and password are required'}), 400

    user = User.query.filter_by(email=email).first()
    if not user or not user.check_password(password):
        return jsonify({'success': False, 'message': 'Invalid email or password'}), 401

    token = generate_token(user.id, user.role)
    return jsonify({
        'success': True,
        'message': 'Login successful',
        'data': {'token': token, 'user': user.to_dict()}
    })


@auth_bp.route('/me', methods=['GET'])
@token_required
def me(current_user):
    return jsonify({'success': True, 'data': current_user.to_dict()})
