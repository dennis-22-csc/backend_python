import os

from dotenv import load_dotenv

GMAIL_SMTP_SETTINGS = {
    'HOST': os.getenv('GMAIL_HOST'),
    'PORT': os.getenv('GMAIL_PORT'),
    'USERNAME': os.getenv('GMAIL_USERNAME'),
    'PASSWORD': os.getenv('GMAIL_PASSWORD'),
    'EMAIL': os.getenv('GMAIL_ADDRESS')
}