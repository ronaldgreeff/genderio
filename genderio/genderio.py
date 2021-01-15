import os
import sys
from dotenv import load_dotenv

dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)

from app import create_app, db, mail
from app.models import User, Baby, BabyImg

app = create_app(os.getenv('FLASK_CONFIG') or default)
