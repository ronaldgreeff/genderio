import os
from itsdangerous import URLSafeSerializer, BadData, BadSignature
from flask import Flask
from project.config import Config


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
