from flask import Blueprint, jsonify
from app.services.notification import send_bid_alert

notification_bp = Blueprint('notifications', __name__)

@notification_bp.route('/send_notification', methods=['POST'])
def send_notification():
    send_bid_alert(item, user)
    return jsonify({'message': 'Notification sent successfully'}), 200
