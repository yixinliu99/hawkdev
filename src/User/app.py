from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

import jwt
import datetime

app = Flask(__name__)

# Database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:root@localhost/userdb'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize SQLAlchemy
db = SQLAlchemy(app)

# Enable CORS for all routes and all origins
CORS(app)

# Define User model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    phone_number = db.Column(db.String(20), nullable=False)
    address = db.Column(db.String(255), nullable=False)
    password = db.Column(db.String(255), nullable=False)
    user_type = db.Column(db.String(20), nullable=False)

    def __repr__(self):
        return f'<User {self.name}>'

# User sign-up endpoint
@app.route("/api/users/signup", methods=["POST"])
def signup():
    data = request.get_json()

    # Extract the data from the request
    name = data.get('name')
    email = data.get('email')
    phone_number = data.get('phoneNumber')
    address = data.get('address')
    password = data.get('password')
    user_type = data.get('userType')

    # Hash the password using the default 'pbkdf2:sha256' method
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
        return jsonify({"message": "Error creating user: " + str(e)}), 500

# User login endpoint
@app.route("/api/users/login", methods=["POST"])
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

if __name__ == "__main__":
    # Initialize the database if not already created
    with app.app_context():
        db.create_all()

    app.run(debug=True, port=5001)
