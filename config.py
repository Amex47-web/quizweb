import os
from dotenv import load_dotenv

load_dotenv()  

class Config:
    # Flask configuration
    SECRET_KEY = os.getenv('SECRET_KEY', 'quizweb')
    FLASK_ENV = os.getenv('FLASK_ENV', 'production')
    DEBUG = os.getenv('DEBUG', 'False') == 'True'

    # MongoDB configuration
    MONGO_URI = os.getenv('MONGO_URI')
    DATABASE_NAME = os.getenv('DATABASE_NAME', 'ketandayke')

    if not MONGO_URI:
        raise ValueError("MONGO_URI is not set in the .env file")

    # Google Auth configuration
    GOOGLE_CLIENT_ID = os.getenv('GOOGLE_CLIENT_ID')
    GOOGLE_CLIENT_SECRET = os.getenv('GOOGLE_CLIENT_SECRET')
    GOOGLE_DISCOVERY_URL = "https://accounts.google.com/.well-known/openid-configuration"
    REDIRECT_URI = "http://localhost:5000/auth/callback"

    if not GOOGLE_CLIENT_ID or not GOOGLE_CLIENT_SECRET:
        raise ValueError("Google Auth credentials are missing in the .env file")

    # API URL
    API_URL = "https://opentdb.com/api.php"

    # Email configuration
    MAIL_SERVER = os.getenv('MAIL_SERVER', 'smtp.gmail.com')
    MAIL_PORT = os.getenv('MAIL_PORT', 587)
    MAIL_USE_TLS = os.getenv('MAIL_USE_TLS', 'True') == 'True'
    MAIL_USE_SSL = os.getenv('MAIL_USE_SSL', 'False') == 'True'
    MAIL_USERNAME = os.getenv('MAIL_USERNAME')
    MAIL_PASSWORD = os.getenv('MAIL_PASSWORD')
    MAIL_DEFAULT_SENDER = os.getenv('MAIL_DEFAULT_SENDER', MAIL_USERNAME)

    if not MAIL_USERNAME or not MAIL_PASSWORD:
        raise ValueError("Email credentials are missing in the .env file")

config = Config()
