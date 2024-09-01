from email.mime.text import MIMEText
from common.utils import logger
import smtplib
import os

def send_email(user_data):
    try:
        subject = f"Welcome! {user_data.pop('name')}"
        body = user_data.pop('body')
        sender = os.getenv("SENDER_EMAIL")
        recipients = [user_data.pop('send_to')]
        password = os.getenv("EMAIL_PASSWORD")

        msg = MIMEText(body)
        msg['Subject'] = subject
        msg['From'] = sender
        msg['To'] = ', '.join(recipients)
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp_server:
            smtp_server.login(sender, password)
            smtp_server.sendmail(sender, recipients, msg.as_string())
        return True

    except Exception as error:
        logger.info(f"Failed to send a validation email, error '{error}' at provider/mail_provider.")
        return False
