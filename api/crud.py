from typing import List
from .models import UserCreate, UserResponse, ThreadCreate, ThreadResponse, MessageCreate, MessageResponse, ModelSchemaUpload, ModelSchemaResponse
from .dependencies import supabase
from fastapi import HTTPException
from time import datetime


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

async def delete_thread(thread_id: str, user_id: str):
    # First, verify the thread belongs to the user
    thread = await supabase.table('threads').select('*').eq('thread_id', thread_id).single().execute()
    if thread.error:
        return False  # Thread not found or other error
    if thread.data['user_id'] != user_id:
        return False  # Thread does not belong to the user
    # If verification passes, proceed to delete
    response = await supabase.table('threads').delete().eq('thread_id', thread_id).execute()
    if response.error:
        return False  # Error during deletion
    return True  # Successfully deleted

async def create_message(thread_id: str, sender: str, content: str) -> MessageResponse:
    data = {
        "thread_id": thread_id,
        "sender": sender,
        "content": content
    }
    response = await supabase.table('messages').insert(data).execute()
    if response.error:
        raise HTTPException(status_code=400, detail=response.error.message)
    return MessageResponse(**response.data[0])

async def get_messages_for_thread(thread_id: str) -> List[MessageResponse]:
    response = await supabase.table('messages').select('*').eq('thread_id', thread_id).execute()
    if response.error or not response.data:
        raise HTTPException(status_code=404, detail="Messages not found")
    return [MessageResponse(**message) for message in response.data]


# CSV File CRUD operations
async def save_model_schema(user_id: str, filename: str, content: bytes) -> bool:
    # Convert bytes content to a string for database storage
    content_str = content.decode('utf-8')
    
    # Prepare the data for insertion
    data = {
        "user_id": user_id,
        "filename": filename,
        "content": content_str,
        "upload_timestamp": datetime.utcnow().isoformat()  # Assuming you want to store the upload time
    }
    
    # Insert the data into the 'model_schemas' table (or whatever your table is named)
    response = await supabase.table('model_schemas').insert(data).execute()
    
    if response.error:
        print(response.error)  # Log the error for debugging
        return False  # Indicate failure
    
    return True  # Indicate success

async def get_model_schemas_for_user(user_id: str):
    response = await supabase.table('model_schemas').select('*').eq('user_id', user_id).execute()
    
    if response.error:
        print(response.error)  # Log the error for debugging
        return None  # Indicate failure or no data found
    
    return response.data  # Return the list of model schemas


# Replace this placeholder function with your actual password hashing mechanism
def hash_password(password: str) -> str:
    return "hashed_" + password  # This is not secure. Use a proper hashing function like bcrypt.
