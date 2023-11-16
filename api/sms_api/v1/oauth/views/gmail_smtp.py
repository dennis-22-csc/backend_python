import smtplib
from v1.oauth.views.email_service import EmailService
from email.mime.text import MIMEText
from email.utils import formataddr
f
class GmailSMTPService(EmailService):
    def __init__(self, settings):
        self.host = settings['GMAIL_HOST']
        self.port = settings['GMAIL_PORT']
        self.username = settings['GMAIL_USERNAME']
        self.password = settings['GMAIL_PASSWORD']
        self.email = settings['GMAIL_ADDRESS']
        self.org_name = "DennisCode"

    def send_email(self, to_address, subject, body):
        try:	
            # Configure smtp server 
            smtp_connection = smtplib.SMTP(self.host, self.port)
            smtp_connection.starttls()
            smtp_connection.login(self.username, self.password)
        
            # Construct the message 
            message = MIMEText(body)
            message['Subject'] = subject
            message['From'] = formataddr(self.org_name, self.email)
            message['To'] = to_address

            # Send the email
            smtp_connection.sendmail(message['From'], [message['To']], message.as_string())

            # Disconnect from the server
            smtp_connection.quit()
        except smtplib.SMTPException as error:
            pass


