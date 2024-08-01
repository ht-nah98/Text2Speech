import os
from datetime import timedelta

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'your-secret-key'
    PERMANENT_SESSION_LIFETIME = timedelta(minutes=30)
    OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY')
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    DEMO_VOICE_FOLDER = os.path.join(BASE_DIR, 'app', 'static', 'demo_voice')
    SESSION_FILE_DIR = os.path.join(BASE_DIR, 'flask_session')