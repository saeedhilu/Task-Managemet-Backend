from django.core.mail import send_mail
from django.conf import settings

def send_email(subject, message, recipient_list, from_email=None):
    """
    Sends a plain email with a subject and message.
    
    :param subject: Subject of the email
    :param message: Plain text message body
    :param recipient_list: List of recipient email addresses
    :param from_email:  'from' email address
    """
    from_email = from_email or settings.EMAIL_HOST_USER
    send_mail(subject, message, from_email, recipient_list)
