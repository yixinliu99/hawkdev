from flask import Blueprint, jsonify, request
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
import datetime
from app.models.user import User
from db import db

user_bp = Blueprint("users", __name__)

# User sign-up endpoint
@user_bp.route("/signup", methods=["POST"])
def signup():
    data = request.get_json()
    # Extract the data from the request
    username = data.get('username')
    email = data.get('email')
    phone_number = data.get('phone_number')
    address = data.get('address')
    password = data.get('password')
    user_type = data.get('user_type')

    # Hash the password using the default 'pbkdf2:sha256' method
    hashed_password = generate_password_hash(password, method="pbkdf2:sha256")

    # Create a new user instance
    new_user = User(
        username=username,
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
        return jsonify({"message": "Error creating user: " + str(e)}), 500

# User login endpoint
@user_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json()

    # Extract the data from the request
    email = data.get('email').strip() 
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
    }, 'supersecretkey', algorithm='HS256')
    return jsonify({'token': token}), 200

# Fetch user profile
@user_bp.route("/profile", methods=["GET"])
def get_profile():
    token = request.headers.get('Authorization')
    if not token:
        return jsonify({"message": "Missing token"}), 401

    try:
        #decoded = token.split(" ")[1]
        decoded = jwt.decode(token.split(" ")[1], 'supersecretkey', algorithms=['HS256']) 
        user_id = decoded.get("user_id")
        user = User.query.get(user_id)
        if not user:
            return jsonify({"message": "User not found"}), 404

        return jsonify({
            "id": user.id,
            "name": user.username,
            "email": user.email,
            "phoneNumber": user.phone_number,
            "address": user.address,
            "userType": user.user_type
        }), 200

    except jwt.ExpiredSignatureError:
        return jsonify({"message": "Token has expired"}), 401
    except Exception as e:
        return jsonify({"message": "Invalid token"}), 401

# Update user profile
@user_bp.route("/profile", methods=["PUT"])
def update_profile():
    token = request.headers.get('Authorization')
    if not token:
        return jsonify({"message": "Missing token"}), 401

    try:
        decoded = jwt.decode(token.split(" ")[1], 'supersecretkey', algorithms=['HS256'])
        user_id = decoded.get("user_id")
        user = User.query.get(user_id)
        if not user:
            return jsonify({"message": "User not found"}), 404

        data = request.get_json()
        user.username = data.get("name", user.username)
        user.phone_number = data.get("phone_number", user.phone_number)
        user.address = data.get("address", user.address)
        user.user_type = data.get("user_type", user.user_type)

        if "password" in data and data["password"]:
            user.password = generate_password_hash(data["password"], method="pbkdf2:sha256")
        db.session.commit()

        return jsonify({"message": "Profile updated successfully"}), 200

    except jwt.ExpiredSignatureError:
        return jsonify({"message": "Token has expired"}), 401
    except Exception as e:
        return jsonify({"message": "Invalid token"}), 401
