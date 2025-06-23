from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class Hash:
    @staticmethod
    def get_password_hash(password: str):
        return pwd_context.hash(password)

    @staticmethod
    def verify(plain_pw: str, hashed_pw: str):
        return pwd_context.verify(plain_pw, hashed_pw)
