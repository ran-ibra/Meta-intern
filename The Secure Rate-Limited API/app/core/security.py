from datetime import datetime, timedelta, timezone
from jose import jwt
from app.core.config import settings
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError

ph = PasswordHasher()

def hash_password(password: str) -> str:
    password = password.strip()
    return ph.hash(password)

def verify_password(password: str, hashed: str) -> bool:
    try:
        return ph.verify(hashed, password.strip())
    except VerifyMismatchError:
        return False

def create_access_token(subject: str) -> str:
    expire = datetime.now(timezone.utc) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    payload = {"sub": subject, "exp": expire}
    return jwt.encode(payload, settings.JWT_SECRET, algorithm=settings.JWT_ALG)
