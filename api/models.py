from pydantic import BaseModel, UUID4, EmailStr, Field
from typing import Optional
from datetime import datetime
from fastapi import UploadFile

# User Models
class UserBase(BaseModel):
    username: str
    email: EmailStr

class UserCreate(UserBase):
    password: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str
    
class UserResponse(UserBase):
    user_id: UUID4
    created_at: datetime
    last_login: Optional[datetime]

    class Config:
        orm_mode = True

# Thread Models
class ThreadBase(BaseModel):
    title: str

class ThreadCreate(ThreadBase):
    pass

class ThreadResponse(ThreadBase):
    thread_id: UUID4
    user_id: UUID4
    created_at: datetime
    last_updated: datetime

    class Config:
        orm_mode = True

# Message Models
class MessageCreate(BaseModel):
    thread_id: UUID4
    sender: str
    content: str

class MessageResponse(MessageCreate):
    message_id: UUID4
    timestamp: datetime

    class Config:
        orm_mode = True

# Model Schema Upload Models
class ModelSchemaUpload(BaseModel):
    schema_name: Optional[str] = Field(None, title="Name of the Model Schema")
    file: UploadFile = Field(..., title="CSV File containing the Model Schema")

class ModelSchemaResponse(BaseModel):
    schema_id: UUID4
    user_id: UUID4
    schema_name: Optional[str]
    file_name: str
    upload_timestamp: datetime
    content_type: str

    class Config:
        orm_mode = True
