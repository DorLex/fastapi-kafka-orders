from fastapi.security import OAuth2PasswordBearer

oauth2_scheme: OAuth2PasswordBearer = OAuth2PasswordBearer(tokenUrl='/auth/token/')
