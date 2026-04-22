import uuid
import jwt
import logging

from passlib.context import CryptContext
from datetime import datetime, timedelta
from itsdangerous import URLSafeTimedSerializer

from FastAPI.Ssali_Jonathan.CRUD.core.config import get_settings

settings = get_settings()

passwd_context = CryptContext(
    schemes=['bcrypt']
)

ACCESS_TOKEN_EXPIRY = 3600

def generate_paswd_hash(password: str) -> str:
    hash = passwd_context.hash(password)
    return hash


def verify_password(password: str, hash: str) -> bool:
    return passwd_context.verify(password, hash)


def create_access_token(user_data: dict, expiry: timedelta = None, refresh: bool = False):
    
    payload = {}

    payload['user'] = user_data
    payload['exp'] = datetime.now() + (expiry if expiry is not None else timedelta(seconds=ACCESS_TOKEN_EXPIRY))
    payload['jti'] = str(uuid.uuid4())

    payload['refresh'] = refresh 
    
    token = jwt.encode(
        payload = payload,
        key = settings.jwt_secret,
        algorithm = settings.jwt_algorithm
    )

    print("CREATE SECRET:", settings.jwt_secret)

    return token


def decode_token(token: str) -> dict:

    try:
        token_data = jwt.decode(
            jwt = token,
            key = settings.jwt_secret,
            algorithms = settings.jwt_algorithm
        )

        print("DECODE SECRET:", settings.jwt_secret)

        return token_data
    
    except jwt.PyJWTError as e:
        logging.exception(e)
        return None


# serializer = URLSafeTimedSerializer(
#     secret_key=settings.jwt_secret
# )


# def create_url_safe_token(data: dict):

#     token = serializer.dumps(data)

#     return token


# def decode_url_safe_token(token: str):
#     try:
#         token_data = serializer.loads(token)
#         return token_data
#     except Exception as e:
#         logging.error(str(e))
#         return None


def get_serializer():
    return URLSafeTimedSerializer(settings.jwt_secret)


def create_url_safe_token(data: dict):
    print("CREATE SECRET:", settings.jwt_secret)
    return get_serializer().dumps(data, salt="email-configuration")


def decode_url_safe_token(token: str):
    try:
        print("DECODE SECRET:", settings.jwt_secret)
        return get_serializer().loads(token, salt="email-configuration")
    except Exception as e:
        logging.error(f"{type(e).__name__}: {e}")
        return None