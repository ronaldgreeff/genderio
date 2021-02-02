from itsdangerous import URLSafeSerializer, BadData, BadSignature
from flask import Flask#, current_app
from project.config import Config


# app = Flask(__name__)
# app.config.from_object(Config)
# app = current_app._get_current_object()
# serializer = URLSafeSerializer(app.config['SECRET_KEY'])
serializer = URLSafeSerializer(f"{os.getenv('SECRET_KEY')}")


def generate_outcome_token(parent_email, baby_id):
    """Generate token using serialized dict of parent's email address and baby ID"""

    return serializer.dumps({
        'parent_email': parent_email,
        'baby_id': baby_id,
    })


def deserialize_outcome_token(token):
    """Deserialize token and return data"""

    try:
        data = serializer.loads(token)
        return data

    except (BadData, BadSignature):
        return False
