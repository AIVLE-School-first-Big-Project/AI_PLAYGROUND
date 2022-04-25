import jwt
import datetime
import aiplay.settings

def generate_access_token(user):
    access_token_payload = {
        'user_id': user.user_id,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=3),
        'iat': datetime.datetime.utcnow()
    }    

    access_token = get_token(access_token_payload)
    return access_token

def generate_refresh_token(user):
    refresh_token_payload = {
        'user_id': user.user_id,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(weeks=2),
        'iat': datetime.datetime.utcnow()
    }

    refresh_token = get_token(refresh_token_payload)
    return refresh_token

def get_token(payload):
    token = jwt.encode(payload, aiplay.settings.SECRET_KEY, algorithm='HS256')
    return token
