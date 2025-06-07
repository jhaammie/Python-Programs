from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel, EmailStr
from datetime import datetime, timedelta
import jwt
import bcrypt
import yaml
from typing import Optional
from uuid import UUID, uuid4
from hoohoohee import CreateUser, GetUserByEmail

# Load JWT config
with open('config.yml', 'r') as f:
    config = yaml.safe_load(f)
JWT_SECRET = config.get('JWT_SECRET', 'your-secret-key')
JWT_EXPIRATION_DAYS = config.get('JWT_EXPIRATION_DAYS', 1)
JWT_EXPIRATION = timedelta(days=JWT_EXPIRATION_DAYS)

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/login")

class UserBase(BaseModel):
    email: EmailStr
    first_name: str
    last_name: str

class UserCreate(UserBase):
    password: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserResponse(UserBase):
    id: UUID
    created_at: datetime
    updated_at: datetime

class Token(BaseModel):
    access_token: str
    token_type: str
    expires_at: datetime
    user: UserResponse

class TokenData(BaseModel):
    user_id: Optional[UUID] = None

def create_access_token(user_id: UUID) -> tuple[str, datetime]:
    expires_at = datetime.utcnow() + JWT_EXPIRATION
    payload = {
        'user_id': str(user_id),
        'exp': expires_at
    }
    return jwt.encode(payload, JWT_SECRET, algorithm='HS256'), expires_at

async def get_current_user(token: str = Depends(oauth2_scheme)) -> UUID:
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=['HS256'])
        user_id: str = payload.get('user_id')
        if user_id is None:
            raise HTTPException(status_code=401, detail="Invalid authentication credentials")
        return UUID(user_id)
    except (jwt.JWTError, ValueError):
        raise HTTPException(status_code=401, detail="Invalid authentication credentials")

@router.post("/register", response_model=Token)
async def register(user: UserCreate):
    # Check if user exists
    existing_user = GetUserByEmail(user.email)
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    # Hash password
    hashed_password = bcrypt.hashpw(user.password.encode('utf-8'), bcrypt.gensalt())
    
    # Create user with UUID
    user_id = uuid4()
    created_at = datetime.utcnow()
    CreateUser(str(user_id), user.email, hashed_password.decode('utf-8'), user.first_name, user.last_name, created_at)
    
    # Generate token
    access_token, expires_at = create_access_token(user_id)
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "expires_at": expires_at,
        "user": {
            "id": user_id,
            "email": user.email,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "created_at": created_at,
            "updated_at": created_at
        }
    }

@router.post("/login", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    # Get user
    user = GetUserByEmail(form_data.username)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid email or password")
    
    # Verify password
    if not bcrypt.checkpw(form_data.password.encode('utf-8'), user[2].encode('utf-8')):
        raise HTTPException(status_code=401, detail="Invalid email or password")
    
    # Generate token
    access_token, expires_at = create_access_token(UUID(user[0]))
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "expires_at": expires_at,
        "user": {
            "id": UUID(user[0]),
            "email": user[1],
            "first_name": user[3],
            "last_name": user[4],
            "created_at": user[5],
            "updated_at": user[6]
        }
    } 