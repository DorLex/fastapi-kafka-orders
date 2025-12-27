from passlib.context import CryptContext

# TODO: куда положить этот объект?
pwd_context: CryptContext = CryptContext(schemes=['bcrypt'], deprecated='auto')


class PasswordService:
    @classmethod
    def generate_password_hash(cls, raw_password: str) -> str:
        hashed_password: str = pwd_context.hash(raw_password)
        print()
        print(f'{type(hashed_password)=}')
        print()
        return hashed_password

    @classmethod
    def verify_password(cls, raw_password: str, hashed_password: str) -> bool:
        return pwd_context.verify(raw_password, hashed_password)
