from flask import Blueprint, request, jsonify
from flask_jwt_extended import (
    create_access_token, 
    jwt_required, 
    get_jwt_identity,
    get_jwt
)
from config import db
from models import User
from functools import wraps
import re

auth_bp = Blueprint('auth', __name__)

# Input validation helpers
def validate_email(email):
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def validate_password(password):
    if len(password) < 6:
        return False, "Password must be at least 6 characters"
    return True, None

def validate_username(username):
    if len(username) < 3:
        return False, "Username must be at least 3 characters"
    if not re.match(r'^[a-zA-Z0-9_]+$', username):
        return False, "Username can only contain letters, numbers, and underscores"
    return True, None

# Role-based access decorator
def admin_required(f):
    @wraps(f)
    @jwt_required()
    def decorated_function(*args, **kwargs):
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        if not user or user.role != 'admin':
            return jsonify({'error': 'Admin access required'}), 403
        return f(*args, **kwargs)
    return decorated_function


# ==================== AUTH ROUTES ====================

@auth_bp.route('/auth/signup', methods=['POST'])
def signup():
    """Register a new user"""
    data = request.get_json()
    
    if not data:
        return jsonify({'error': 'No data provided'}), 400
    
    username = data.get('username', '').strip()
    email = data.get('email', '').strip().lower()
    password = data.get('password', '')
    role = data.get('role', 'client')
    
    # Validate inputs
    if not username or not email or not password:
        return jsonify({'error': 'Username, email, and password are required'}), 400
    
    valid, msg = validate_username(username)
    if not valid:
        return jsonify({'error': msg}), 400
    
    if not validate_email(email):
        return jsonify({'error': 'Invalid email format'}), 400
    
    valid, msg = validate_password(password)
    if not valid:
        return jsonify({'error': msg}), 400
    
    # Check if user exists
    if User.query.filter_by(email=email).first():
        return jsonify({'error': 'Email already registered'}), 409
    
    if User.query.filter_by(username=username).first():
        return jsonify({'error': 'Username already taken'}), 409
    
    # Validate role
    if role not in ['client', 'provider']:
        role = 'client'
    
    # Create new user
    user = User(username=username, email=email, role=role)
    user.password_hash = password
    
    db.session.add(user)
    db.session.commit()
    
    # Create access token
    access_token = create_access_token(identity=user.id)
    
    return jsonify({
        'message': 'User created successfully',
        'user': user.to_dict(),
        'access_token': access_token
    }), 201


@auth_bp.route('/auth/login', methods=['POST'])
def login():
    """Login user and return JWT token"""
    data = request.get_json()
    
    if not data:
        return jsonify({'error': 'No data provided'}), 400
    
    email = data.get('email', '').strip().lower()
    password = data.get('password', '')
    
    if not email or not password:
        return jsonify({'error': 'Email and password are required'}), 400
    
    # Find user
    user = User.query.filter_by(email=email).first()
    
    if not user or not user.check_password(password):
        return jsonify({'error': 'Invalid email or password'}), 401
    
    if not user.is_active:
        return jsonify({'error': 'Account is deactivated'}), 403
    
    # Create access token
    access_token = create_access_token(identity=user.id)
    
    return jsonify({
        'message': 'Login successful',
        'user': user.to_dict(),
        'access_token': access_token
    }), 200


@auth_bp.route('/auth/me', methods=['GET'])
@jwt_required()
def get_current_user():
    """Get current logged-in user's profile"""
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    
    if not user:
        return jsonify({'error': 'User not found'}), 404
    
    return jsonify(user.to_dict()), 200


@auth_bp.route('/auth/me', methods=['PATCH'])
@jwt_required()
def update_profile():
    """Update current user's profile"""
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    
    if not user:
        return jsonify({'error': 'User not found'}), 404
    
    data = request.get_json()
    
    if 'username' in data:
        username = data['username'].strip()
        valid, msg = validate_username(username)
        if not valid:
            return jsonify({'error': msg}), 400
        existing = User.query.filter_by(username=username).first()
        if existing and existing.id != user.id:
            return jsonify({'error': 'Username already taken'}), 409
        user.username = username
    
    if 'email' in data:
        email = data['email'].strip().lower()
        if not validate_email(email):
            return jsonify({'error': 'Invalid email format'}), 400
        existing = User.query.filter_by(email=email).first()
        if existing and existing.id != user.id:
            return jsonify({'error': 'Email already registered'}), 409
        user.email = email
    
    if 'image_url' in data:
        user.image_url = data['image_url']
    
    db.session.commit()
    
    return jsonify({
        'message': 'Profile updated',
        'user': user.to_dict()
    }), 200


@auth_bp.route('/auth/change-password', methods=['POST'])
@jwt_required()
def change_password():
    """Change user's password"""
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    
    if not user:
        return jsonify({'error': 'User not found'}), 404
    
    data = request.get_json()
    current_password = data.get('current_password', '')
    new_password = data.get('new_password', '')
    
    if not user.check_password(current_password):
        return jsonify({'error': 'Current password is incorrect'}), 401
    
    valid, msg = validate_password(new_password)
    if not valid:
        return jsonify({'error': msg}), 400
    
    user.password_hash = new_password
    db.session.commit()
    
    return jsonify({'message': 'Password changed successfully'}), 200


# ==================== USER BOOKINGS ====================

@auth_bp.route('/auth/my-bookings', methods=['GET'])
@jwt_required()
def get_my_bookings():
    """Get current user's bookings"""
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    
    if not user:
        return jsonify({'error': 'User not found'}), 404
    
    bookings = [b.to_dict() for b in user.bookings]
    return jsonify(bookings), 200


@auth_bp.route('/auth/my-bookings/<int:booking_id>', methods=['PATCH'])
@jwt_required()
def update_my_booking(booking_id):
    """Update user's own booking (cancel or request reschedule)"""
    from models import Booking
    
    user_id = get_jwt_identity()
    booking = Booking.query.get(booking_id)
    
    if not booking:
        return jsonify({'error': 'Booking not found'}), 404
    
    if booking.client_id != user_id:
        return jsonify({'error': 'You can only modify your own bookings'}), 403
    
    data = request.get_json()
    
    if 'status' in data:
        new_status = data['status']
        # Users can only cancel their bookings
        if new_status == 'cancelled':
            booking.status = 'cancelled'
        elif new_status == 'reschedule_requested':
            booking.status = 'reschedule_requested'
        else:
            return jsonify({'error': 'Invalid status change'}), 400
    
    if 'notes' in data:
        booking.notes = data['notes']
    
    db.session.commit()
    
    return jsonify({
        'message': 'Booking updated',
        'booking': booking.to_dict()
    }), 200


# ==================== ADMIN USER MANAGEMENT ====================

@auth_bp.route('/admin/users', methods=['GET'])
@admin_required
def admin_get_users():
    """Admin: Get all users"""
    users = User.query.all()
    return jsonify([u.to_dict() for u in users]), 200


@auth_bp.route('/admin/users/<int:user_id>', methods=['PATCH'])
@admin_required
def admin_update_user(user_id):
    """Admin: Update user (role, active status)"""
    user = User.query.get(user_id)
    
    if not user:
        return jsonify({'error': 'User not found'}), 404
    
    data = request.get_json()
    
    if 'role' in data:
        if data['role'] in ['client', 'provider', 'admin']:
            user.role = data['role']
    
    if 'is_active' in data:
        user.is_active = bool(data['is_active'])
    
    db.session.commit()
    
    return jsonify({
        'message': 'User updated',
        'user': user.to_dict()
    }), 200


@auth_bp.route('/admin/users/<int:user_id>', methods=['DELETE'])
@admin_required
def admin_delete_user(user_id):
    """Admin: Delete user"""
    user = User.query.get(user_id)
    
    if not user:
        return jsonify({'error': 'User not found'}), 404
    
    db.session.delete(user)
    db.session.commit()
    
    return jsonify({'message': 'User deleted'}), 200


@auth_bp.route('/admin/bookings', methods=['GET'])
@admin_required
def admin_get_all_bookings():
    """Admin: Get all bookings"""
    from models import Booking
    bookings = Booking.query.all()
    return jsonify([b.to_dict() for b in bookings]), 200


@auth_bp.route('/admin/bookings/<int:booking_id>', methods=['DELETE'])
@admin_required
def admin_delete_booking(booking_id):
    """Admin: Delete a booking"""
    from models import Booking
    booking = Booking.query.get(booking_id)
    
    if not booking:
        return jsonify({'error': 'Booking not found'}), 404
    
    db.session.delete(booking)
    db.session.commit()
    
    return jsonify({'message': 'Booking deleted'}), 200
