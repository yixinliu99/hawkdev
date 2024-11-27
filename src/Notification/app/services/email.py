import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def send_email_notification(user, item_name, message):
    user_email = user.email

    subject = f"Notification for {item_name}"
    body = f"Hello {user.name},\n\n{message}\n\nBest regards,\nYour Notification Service"

    sender_email = "no-reply@example.com"
    receiver_email = user_email

    msg = MIMEMultipart()
    msg["From"] = sender_email
    msg["To"] = receiver_email
    msg["Subject"] = subject
    msg.attach(MIMEText(body, "plain"))

    try:
        server = smtplib.SMTP("smtp.example.com", 587)
        server.starttls()
        server.login(sender_email, "email-password")
        server.sendmail(sender_email, receiver_email, msg.as_string())
        server.close()
        print("Email sent successfully!")
    except Exception as e:
        print(f"Failed to send email: {str(e)}")
