import jwt
from django.conf import settings
from datetime import datetime, timedelta
from .models import User
JWT_SECRET = settings.SECRET_KEY
JWT_ALGORITHM = 'HS256'
JWT_EXP_DELTA_DAYS = 10

def get_token(user):
    payload = {
        'user_id': user.id,
        'exp': datetime.utcnow() + timedelta(days=JWT_EXP_DELTA_DAYS)
        # 'exp': datetime.utcnow() + timedelta(seconds=300)
    }
    jwt_token = jwt.encode(payload, JWT_SECRET, JWT_ALGORITHM)
    return {'access_token': jwt_token}

def decrypt_token(jwt_token):
    try:
        token = jwt.decode(jwt_token,JWT_SECRET, JWT_ALGORITHM)
        print(token)
        user_id=token["user_id"]
        email = User.objects.get(id=user_id).email
        user = User.objects.get(id=user_id)
        return user
    except :
        return 0
