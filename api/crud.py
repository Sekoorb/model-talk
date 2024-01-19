from typing import List
from .models import UserCreate, UserResponse, ThreadCreate, ThreadResponse, MessageCreate, MessageResponse, CSVFileCreate, CSVFileResponse
from .dependencies import supabase
from fastapi import HTTPException

# User CRUD operations
async def create_user(user: UserCreate) -> UserResponse:
    data = user.model_dump()
    hashed_password = hash_password(data.pop('password'))  # Replace with your password hashing function
    data['password_hash'] = hashed_password
    response = await supabase.table('users').insert(data).execute()
    if response.error:
        raise HTTPException(status_code=400, detail=response.error.message)
    return UserResponse(**response.data[0])

async def authenticate_user(email: str, password: str):
    user = await supabase.table('users').select('*').eq('email', email).single().execute()
    if not user.data:
        return False
    if not verify_password(password, user.data['password_hash']):  # Assume verify_password is defined
        return False
    return user.data

# Placeholder for verify_password function - replace with actual password verification
def verify_password(plain_password, hashed_password):
    return hash_password(plain_password) == hashed_password  # Replace with actual verification logic

async def get_user(user_id: str) -> UserResponse:
    response = await supabase.table('users').select('*').eq('user_id', user_id).single().execute()
    if response.error:
        raise HTTPException(status_code=404, detail="User not found")
    return UserResponse(**response.data)

# Thread CRUD operations
async def create_thread(user_id: str, thread: ThreadCreate) -> ThreadResponse:
    data = thread.model_dump()
    data['user_id'] = user_id
    response = await supabase.table('threads').insert(data).execute()
    if response.error:
        raise HTTPException(status_code=400, detail=response.error.message)
    return ThreadResponse(**response.data[0])

async def get_threads_for_user(user_id: str) -> List[ThreadResponse]:
    response = await supabase.table('threads').select('*').eq('user_id', user_id).execute()
    if response.error:
        raise HTTPException(status_code=404, detail="Threads not found")
    return [ThreadResponse(**thread) for thread in response.data]

# Message CRUD operations
async def create_message(message: MessageCreate) -> MessageResponse:
    data = message.model_dump()
    response = await supabase.table('messages').insert(data).execute()
    if response.error:
        raise HTTPException(status_code=400, detail=response.error.message)
    return MessageResponse(**response.data[0])

async def get_messages_for_thread(thread_id: str) -> List[MessageResponse]:
    response = await supabase.table('messages').select('*').eq('thread_id', thread_id).execute()
    if response.error:
        raise HTTPException(status_code=404, detail="Messages not found")
    return [MessageResponse(**message) for message in response.data]

# CSV File CRUD operations
async def upload_csv_file(csv_file: CSVFileCreate, user_id: str) -> CSVFileResponse:
    data = csv_file.model_dump()
    data['user_id'] = user_id
    response = await supabase.table('csv_files').insert(data).execute()
    if response.error:
        raise HTTPException(status_code=400, detail=response.error.message)
    return CSVFileResponse(**response.data[0])

async def get_csv_files_for_user(user_id: str) -> List[CSVFileResponse]:
    response = await supabase.table('csv_files').select('*').eq('user_id', user_id).execute()
    if response.error:
        raise HTTPException(status_code=404, detail="CSV files not found")
    return [CSVFileResponse(**file) for file in response.data]

# Replace this placeholder function with your actual password hashing mechanism
def hash_password(password: str) -> str:
    return "hashed_" + password  # This is not secure. Use a proper hashing function like bcrypt.
