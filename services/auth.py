from datetime import datetime, timedelta, timezone
from typing import Optional
from fastapi import HTTPException, status, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import JWTError, jwt
from passlib.context import CryptContext
from motor.motor_asyncio import AsyncIOMotorDatabase

from db import get_database
from models.user import UserInDB, serialize_user_in_db
from schemas import TokenData
from settings import get_settings

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Security scheme
security = HTTPBearer()

settings = get_settings()


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a plain password against its hash."""
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    """Generate password hash."""
    # bcrypt has a 72-byte limit, truncate if necessary
    if len(password.encode('utf-8')) > 72:
        password = password[:72]
    return pwd_context.hash(password)


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """Create JWT access token."""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=settings.jwt_access_token_expire_minutes)
    
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.jwt_secret_key, algorithm=settings.jwt_algorithm)
    return encoded_jwt


async def authenticate_user(db: AsyncIOMotorDatabase, username: str, password: str) -> Optional[UserInDB]:
    """Authenticate user with username/password."""
    print(f"🔐 Authenticating user: {username}")
    
    # Import here to avoid circular dependency
    from services.users import get_user_by_username
    
    user = await get_user_by_username(db, username)
    if not user:
        print(f"❌ User not found: {username}")
        return None
    print(f"✅ User found: {username}")
    print(f"🔑 Verifying password...")
    
    password_match = verify_password(password, user.hashed_password)
    print(f"🔑 Password hash: {user.hashed_password[:20]}...")
    print(f"🔑 Password match result: {password_match}")
    
    if not password_match:
        print(f"❌ Password verification failed for user: {username}")
        return None
    print(f"✅ Password verified for user: {username}")
    return user


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: AsyncIOMotorDatabase = Depends(get_database)
) -> UserInDB:
    """Get current authenticated user from JWT token."""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        token = credentials.credentials
        payload = jwt.decode(token, settings.jwt_secret_key, algorithms=[settings.jwt_algorithm])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    
    # Import here to avoid circular dependency
    from services.users import get_user_by_username
    
    user = await get_user_by_username(db, username=token_data.username)
    if user is None:
        raise credentials_exception
    return user


async def get_current_active_user(current_user: UserInDB = Depends(get_current_user)) -> UserInDB:
    """Get current active user."""
    if not current_user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


async def get_current_admin_user(current_user: UserInDB = Depends(get_current_active_user)) -> UserInDB:
    """Get current admin user."""
    if not current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    return current_user
