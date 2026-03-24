from passlib.context import CryptContext
import hashlib

pwd_context = CryptContext(
    schemes=["bcrypt"], deprecated="auto", bcrypt__truncate_error=False
)


def hash_password(password: str) -> str:
    hash_password = hashlib.sha256(password.encode("utf-8"))
    return pwd_context.hash(hash_password.hexdigest())
