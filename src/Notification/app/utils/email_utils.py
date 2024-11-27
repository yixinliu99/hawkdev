import sendgrid
from sendgrid.helpers.mail import Mail, Email, To, Content
from app.config import Config

def send_email(to_email, subject, body):
    sg = sendgrid.SendGridAPIClient(api_key=Config.EMAIL_API_KEY)
    from_email = Email("no-reply@auction.com")
    to_email = To(to_email)
    content = Content("text/plain", body)
    mail = Mail(from_email, to_email, subject, content)

    try:
        response = sg.send(mail)
        return response.status_code
    except Exception as e:
        print(f"Error sending email: {e}")
        return None
