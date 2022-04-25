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

# 토큰이 유효하면 payload를 반환하고, 유효하지 않으면 False를 반환
def verify_token(token):    
    try:
        payload = jwt.decode(token, aiplay.settings.SECRET_KEY, algorithms=['HS256'])
        return payload
    except jwt.exceptions.InvalidSignatureError as e:
        print(e)
    except jwt.exceptions.ExpiredSignatureError as e:
        print(e)
    except jwt.exceptions.InvalidTokenError as e:
        print(e)
    return False
