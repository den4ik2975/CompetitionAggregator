from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext

SECRET_KEY = "b47f886c15c649ce3aded78f36f983ea"  # Replace with a secure secret key
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth")

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
