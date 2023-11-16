import smtplib
from email.mime.text import MIMEText
from flask import abort
from email.utils import formataddr
import os

from dotenv import load_dotenv

class GmailSMTPService:
    def __init__(self):
        self.host = os.getenv('GMAIL_HOST')
        self.port = os.getenv('GMAIL_PORT')
        self.username = os.getenv('GMAIL_USERNAME')
        self.password = os.getenv('GMAIL_PASSWORD')
        self.email = os.getenv('GMAIL_ADDRESS')
        self.org_name = os.getenv('C')
        
    def send_email(self, to_address, subject, body):
        try:	
            # Configure smtp server 
            smtp_connection = smtplib.SMTP(self.host, self.port)
            smtp_connection.starttls()
            smtp_connection.login(self.username, self.password)
        
            # Construct the message 
            message = MIMEText(body)
            message['Subject'] = subject
            message['From'] = formataddr((self.org_name, self.email))
            message['To'] = to_address

            # Send the email
            smtp_connection.sendmail(message['From'], [message['To']], message.as_string())

            # Disconnect from the server
            smtp_connection.quit()
            
        except smtplib.SMTPException:
            error_info = ["Email Error", "Error occurred in emailing code"]
            abort(500, error_info)


