from flask import Blueprint, jsonify, request
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
import datetime
from app.models.user import User
from db import db, mongo
import requests

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

@user_bp.route("/watchlist", methods=["POST"])
def add_to_watchlist():
    token = request.headers.get('Authorization')
    if not token:
        return jsonify({"message": "Missing token"}), 401

    try:
        decoded = jwt.decode(token.split(" ")[1], 'supersecretkey', algorithms=['HS256'])
        user_id = decoded.get("user_id")
        
        # Fetch user from MySQL
        user = User.query.get(user_id)
        if not user:
            return jsonify({"message": "User not found"}), 404

        data = request.get_json()
        item_id = data.get("item_id")
        keyword = data.get("keyword")  # User-defined keyword
        category = data.get("category")  # User-defined category

        # Store watchlist in MongoDB
        watchlist_item = {
            "user_id": user_id,
            "item_id": item_id,
            "keyword": keyword,
            "category": category
        }

        mongo.db.watchlist.insert_one(watchlist_item)
        return jsonify({"message": "Item added to watchlist"}), 200

    except jwt.ExpiredSignatureError:
        return jsonify({"message": "Token has expired"}), 401
    except Exception as e:
        return jsonify({"message": "Error adding item to watchlist: " + str(e)}), 500

# Get user's watchlist (MongoDB)
@user_bp.route("/watchlist", methods=["GET"])
def get_watchlist():
    token = request.headers.get('Authorization')
    if not token:
        return jsonify({"message": "Missing token"}), 401

    try:
        decoded = jwt.decode(token.split(" ")[1], 'supersecretkey', algorithms=['HS256'])
        user_id = decoded.get("user_id")

        # Retrieve watchlist from MongoDB
        watchlist_items_cursor = mongo.db.watchlist.find({"userId": user_id})
        watchlist_items = list(watchlist_items_cursor)  # Convert cursor to a list

        # Bulk fetch item details
        item_ids = [watchlist_item['itemId'] for watchlist_item in watchlist_items]
        items_in_bulk = mongo.db.items.find({"_id": {"$in": item_ids}})

        # Create a dictionary to quickly lookup items by ID
        item_dict = {str(item['_id']): item for item in items_in_bulk}

        items = []
        for watchlist_item in watchlist_items:
            item = item_dict.get(str(watchlist_item['itemId']))
            if item:
                items.append({
                    "item_id": item['_id'],
                    "item_name": item['name'],
                    "keyword": watchlist_item.get('keyword', ''),  # Use .get() to handle missing fields
                    "category": watchlist_item.get('category', '')
                })
            else:
                # If item not found in item service, add a placeholder or skip
                items.append({
                    "item_id": watchlist_item['itemId'],
                    "item_name": "Item not found",
                    "keyword": watchlist_item.get('keyword', ''),
                    "category": watchlist_item.get('category', '')
                })

        return jsonify({"watchlist": items}), 200
    except jwt.ExpiredSignatureError:
        return jsonify({"message": "Token has expired"}), 401
    except Exception as e:
        return jsonify({"message": "Error fetching watchlist: " + str(e)}), 500

# Remove item from watchlist (MongoDB)
@user_bp.route("/watchlist", methods=["DELETE"])
def remove_from_watchlist():
    token = request.headers.get('Authorization')
    if not token:
        return jsonify({"message": "Missing token"}), 401

    try:
        decoded = jwt.decode(token.split(" ")[1], 'supersecretkey', algorithms=['HS256'])
        user_id = decoded.get("user_id")

        # Fetch user from MySQL
        user = User.query.get(user_id)
        if not user:
            return jsonify({"message": "User not found"}), 404

        data = request.get_json()
        item_id = data.get("item_id")

        # Remove item from the user's watchlist in MongoDB
        result = mongo.db.watchlist.delete_one({"user_id": user_id, "item_id": item_id})
        if result.deleted_count == 0:
            return jsonify({"message": "Item not found in watchlist"}), 404

        return jsonify({"message": "Item removed from watchlist"}), 200

    except jwt.ExpiredSignatureError:
        return jsonify({"message": "Token has expired"}), 401
    except Exception as e:
        return jsonify({"message": "Error removing item from watchlist: " + str(e)}), 500


@user_bp.route("/cart", methods=["POST"])
def add_to_cart():
    token = request.headers.get('Authorization')
    if not token:
        return jsonify({"message": "Missing token"}), 401

    try:
        # Decode the token to get user ID
        decoded = jwt.decode(token.split(" ")[1], 'supersecretkey', algorithms=['HS256'])
        user_id = decoded.get("user_id")

        # Extract item ID and quantity from the request
        data = request.get_json()
        item_id = data.get("item_id")
        quantity = data.get("quantity", 1)  # Default to 1 if not provided

        if not item_id:
            return jsonify({"message": "Item ID is required"}), 400

        # Fetch item details from item microservice
        item_service_url = f"http://localhost:8081/api/items/{item_id}"  # Adjust this URL
        item_response = requests.get(item_service_url)

        if item_response.status_code != 200:
            return jsonify({"message": "Item not found in item service"}), 404

        item_data = item_response.json()

        # Check if the item already exists in the cart
        cart_item = mongo.db.cart.find_one({"user_id": user_id, "item_id": item_id})
        if cart_item:
            # Increment quantity if the item already exists
            mongo.db.cart.update_one(
                {"user_id": user_id, "item_id": item_id},
                {"$inc": {"quantity": quantity}}
            )
        else:
            # Insert the item into the cart with full details
            mongo.db.cart.insert_one({
                "user_id": user_id,
                "item_id": item_id,
                "shipping_cost": item_data.get('shipping_cost'),  
                "description": item_data.get('description'),
                "flagged": item_data.get('flagged'),
                "category": item_data.get('category'),
                "keywords": item_data.get('keywords'),
                "starting_price": item_data.get('starting_price'),
                "quantity": quantity  # Use the quantity from the request
            })

        return jsonify({"message": "Item added to cart"}), 200

    except jwt.ExpiredSignatureError:
        return jsonify({"message": "Token has expired"}), 401
    except Exception as e:
        return jsonify({"message": "Error adding item to cart: " + str(e)}), 500


@user_bp.route("/cart", methods=["GET"])
def get_cart():
    token = request.headers.get('Authorization')
    if not token:
        return jsonify({"message": "Missing token"}), 401

    try:
        decoded = jwt.decode(token.split(" ")[1], 'supersecretkey', algorithms=['HS256'])
        user_id = decoded.get("user_id")
        cart_items = list(mongo.db.cart.find({"user_id": user_id}))

        return jsonify({"cart": cart_items}), 200
    except jwt.ExpiredSignatureError:
        return jsonify({"message": "Token has expired"}), 401
    except Exception as e:
        return jsonify({"message": "Error fetching cart: " + str(e)}), 500

@user_bp.route("/cart", methods=["DELETE"])
def remove_from_cart():
    token = request.headers.get('Authorization')
    if not token:
        return jsonify({"message": "Missing token"}), 401

    try:
        decoded = jwt.decode(token.split(" ")[1], 'supersecretkey', algorithms=['HS256'])
        user_id = decoded.get("user_id")
        data = request.get_json()
        item_id = data.get("item_id")

        result = mongo.db.cart.delete_one({"user_id": user_id, "item_id": item_id})
        if result.deleted_count == 0:
            return jsonify({"message": "Item not found in cart"}), 404

        return jsonify({"message": "Item removed from cart"}), 200

    except jwt.ExpiredSignatureError:
        return jsonify({"message": "Token has expired"}), 401
    except Exception as e:
        return jsonify({"message": "Error removing item from cart: " + str(e)}), 500


@user_bp.route("/cart/checkout", methods=["GET"])
def checkout_cart():
    token = request.headers.get('Authorization')
    if not token:
        return jsonify({"message": "Missing token"}), 401

    try:
        # Decode the token to get user ID
        decoded = jwt.decode(token.split(" ")[1], 'supersecretkey', algorithms=['HS256'])
        user_id = decoded.get("user_id")

        # Retrieve user's cart items from MongoDB
        cart_items = mongo.db.cart.find({"user_id": user_id})
        
        if not cart_items:
            return jsonify({"message": "Cart is empty"}), 400

        total_amount = 0  # Initialize total amount

        items = []
        for cart_item in cart_items:
            item_id = cart_item.get("item_id")
            #item_name = cart_item.get("item_name")
            item_price = cart_item.get("starting_price", 0)
            quantity = cart_item.get("quantity", 1)
            shipping_cost = cart_item.get("shipping_cost", 0)

            # Calculate the item total (price * quantity + shipping)
            item_total = (item_price + shipping_cost) * quantity

            # Add the item total to the overall total
            total_amount += item_total

            items.append({
                "item_id": item_id,
                #"item_name": item_name,
                "quantity": quantity,
                "price": item_price,
                "shipping_cost": shipping_cost,
                "item_total": item_total
            })

        # Add total amount to the response
        return jsonify({
            "cart_items": items,
            "total_amount": total_amount
        }), 200

    except jwt.ExpiredSignatureError:
        return jsonify({"message": "Token has expired"}), 401
    except Exception as e:
        return jsonify({"message": "Error fetching cart: " + str(e)}), 500


@user_bp.route("/cart/checkout", methods=["POST"])
def process_checkout():
    token = request.headers.get('Authorization')
    if not token:
        return jsonify({"message": "Missing token"}), 401

    try:
        # Decode the token to get the user ID
        decoded = jwt.decode(token.split(" ")[1], 'supersecretkey', algorithms=['HS256'])
        user_id = decoded.get("user_id")

        # Fetch user's cart from MongoDB
        cart_items = mongo.db.cart.find({"user_id": user_id})

        if not cart_items:
            return jsonify({"message": "Cart is empty"}), 400

        total_amount = 0
        order_items = []

        # Calculate the total amount and prepare order items using details already in the cart
        for cart_item in cart_items:
            item_id = cart_item["item_id"]
            quantity = cart_item["quantity"]

            # Fetch item details from the cart entry itself
            #item_name = cart_item.get("item_name")  
            item_price = cart_item.get("starting_price")
            shipping_cost = cart_item.get("shipping_cost")

            if not item_price is None or shipping_cost is None:
                return jsonify({"message": f"Item {item_id} missing necessary details"}), 400

            # Calculate the total for this item
            item_total = (item_price + shipping_cost) * quantity
            total_amount += item_total

            order_items.append({
                "item_id": item_id,
                "quantity": quantity,
                #"item_name": item_name,
                "total_price": item_total
            })

        # Proceed with order creation (could be stored in a separate collection or service)
        order = {
            "user_id": user_id,
            "total_amount": total_amount,
            "items": order_items,
            "status": "processing",
            "created_at": datetime.datetime.utcnow()
        }
        
        # Store order in the database
        mongo.db.orders.insert_one(order)

        # Clear the cart after checkout
        mongo.db.cart.delete_many({"user_id": user_id})

        return jsonify({"message": "Checkout successful", "order_id": str(order["_id"])}), 200

    except jwt.ExpiredSignatureError:
        return jsonify({"message": "Token has expired"}), 401
    except Exception as e:
        return jsonify({"message": "Error processing checkout: " + str(e)}), 500
