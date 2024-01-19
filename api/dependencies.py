from .config import settings
from supabase import create_client, Client
import jwt
import os
from datetime import datetime, timedelta

# Initialize Supabase client
supabase: Client = create_client(settings.supabase_url, settings.supabase_key)

SECRET_KEY = os.getenv("SECRET_KEY")  # Make sure to have a strong secret key
ALGORITHM = "HS256"  # Algorithm for encoding the JWT

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(hours=1)  # Token expires in 1 hour
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

