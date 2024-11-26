from app.services.email import send_email

def send_bid_alert(item, user):
    subject = f"New bid on your item: {item.name}"
    body = f"Someone has bid on your item '{item.name}'. Check it out now!"
    send_email(subject, body, user.email)
