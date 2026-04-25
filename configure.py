import os
from dotenv import load_dotenv

load_dotenv()

class configure:
    SECRET_KEY = os.environ.get('SECRET_KEY','dev-secret-fallback')
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
    SQLALCHEMY_TRACK_MODIFICATIONS = False    # it tracks if anything is modified with the DB objects.
    GOOGLE_CLIENT_ID = os.getenv('GOOGLE_CLIENT_ID')
    GOOGLE_CLIENT_SECRET = os.getenv('GOOGLE_CLIENT_SECRET')