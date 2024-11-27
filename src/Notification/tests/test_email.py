from Notification.app.services.email import send_email

def test_send_email():
    result = send_email('Test Subject', 'Test Body', 'test@example.com')
    assert result is True  
