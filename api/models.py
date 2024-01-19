from pydantic import BaseModel, UUID4, EmailStr
from typing import Optional
from datetime import datetime

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

# CSV File Models
class CSVFileCreate(BaseModel):
    file_name: str
    file_content: str

class CSVFileResponse(CSVFileCreate):
    file_id: UUID4
    user_id: UUID4
    upload_timestamp: datetime
    analysis_status: str
    analysis_results: Optional[str]

    class Config:
        orm_mode = True
