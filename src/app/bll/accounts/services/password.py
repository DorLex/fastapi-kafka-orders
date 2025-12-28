from logging import getLogger, Logger

import bcrypt

logger: Logger = getLogger(__name__)


class PasswordService:
    @classmethod
    def generate_password_hash(cls, raw_password: str) -> str:
        hashed_password: bytes = bcrypt.hashpw(raw_password.encode('utf-8'), bcrypt.gensalt())
        return hashed_password.decode('utf-8')

    @classmethod
    def verify_password(cls, raw_password: str, hashed_password: str) -> bool:
        try:
            return bcrypt.checkpw(
                raw_password.encode('utf-8'),
                hashed_password.encode('utf-8'),
            )
        except Exception as exc:
            logger.warning(f'Ошибка при валидации пароля: {exc}')

        return False
