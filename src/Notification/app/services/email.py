import smtplib
from email.mime.text import MIMEText

def send_email(subject, body, to_email):
    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = 'email@example.com'
    msg['To'] = to_email

    with smtplib.SMTP('smtp.example.com') as server:
        server.login('email@example.com', 'email-password')
        server.sendmail('email@example.com', to_email, msg.as_string())
