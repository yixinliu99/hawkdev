from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
import jwt
import datetime
from app.models.user import User

# Initialize the database and user model (imported from app.py)
#from app import db
from functools import wraps

# Define User model (should be imported from app.py ideally)


# Define the Blueprint for user-related routes
user_bp = Blueprint('user_bp', __name__)

# Decorator to check if the user is authenticated
def token_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        token = request.headers.get('x-access-token')
        if not token:
            return jsonify({'message': 'Token is missing!'}), 403
        try:
            data = jwt.decode(token, 'secret', algorithms=["HS256"])
            current_user = User.query.filter_by(id=data['user_id']).first()
        except Exception as e:
            return jsonify({'message': 'Token is invalid!'}), 403
        return f(current_user, *args, **kwargs)
    return decorated_function

# User sign-up route
@user_bp.route("/signup", methods=["POST"])
def signup():
    data = request.get_json()

    # Extract the data from the request
    name = data.get('name')
    email = data.get('email')
    phone_number = data.get('phoneNumber')
    address = data.get('address')
    password = data.get('password')
    user_type = data.get('userType')

    # Hash the password
    hashed_password = generate_password_hash(password)

    # Create a new user instance
    new_user = User(
        name=name,
        email=email,
        phone_number=phone_number,
        address=address,
        password=hashed_password,
        user_type=user_type
    )

    # Add the user to the database
    try:
        db.session.add(new_user)
        db.session.commit()
        return jsonify({"message": "User created successfully!"}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": f"Error creating user: {str(e)}"}), 500

# User login route
@user_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json()

    # Extract the data from the request
    email = data.get('email')
    password = data.get('password')

    # Find the user by email
    user = User.query.filter_by(email=email).first()

    # Check if user exists and password is correct
    if not user or not check_password_hash(user.password, password):
        return jsonify({"message": "Invalid credentials"}), 401

    # Generate JWT token
    token = jwt.encode({
        'user_id': user.id,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=1)
    }, 'secret', algorithm='HS256')

    return jsonify({'token': token}), 200

# Get user profile
@user_bp.route("/profile", methods=["GET"])
@token_required
def get_profile(current_user):
    # Return user profile data
    user_data = {
        'id': current_user.id,
        'name': current_user.name,
        'email': current_user.email,
        'phone_number': current_user.phone_number,
        'address': current_user.address,
        'user_type': current_user.user_type
    }
    return jsonify({'user': user_data})

# Update user profile
@user_bp.route("/profile", methods=["PUT"])
@token_required
def update_profile(current_user):
    data = request.get_json()

    # Update the user data with the new values
    current_user.name = data.get('name', current_user.name)
    current_user.email = data.get('email', current_user.email)
    current_user.phone_number = data.get('phone_number', current_user.phone_number)
    current_user.address = data.get('address', current_user.address)
    current_user.user_type = data.get('user_type', current_user.user_type)

    # Commit the changes to the database
    db.session.commit()

    return jsonify({'message': 'Profile updated successfully!'}), 200
