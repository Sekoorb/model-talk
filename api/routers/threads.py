from fastapi import APIRouter, Depends, HTTPException, status
from ..models import ThreadCreate, ThreadResponse
from ..crud import create_thread, get_threads_for_user, delete_thread
from ..dependencies import get_current_user

router = APIRouter()

@router.post("/threads/", response_model=ThreadResponse, status_code=status.HTTP_201_CREATED)
async def create_new_thread(thread: ThreadCreate, user_id: str = Depends(get_current_user)):
    created_thread = await create_thread(user_id, thread)
    if not created_thread:
        raise HTTPException(status_code=400, detail="Error creating thread")
    return created_thread

@router.get("/threads/", response_model=list[ThreadResponse])
async def list_threads(user_id: str = Depends(get_current_user)):
    threads = await get_threads_for_user(user_id)
    if not threads:
        raise HTTPException(status_code=404, detail="No threads found")
    return threads

@router.delete("/threads/{thread_id}", status_code=status.HTTP_204_NO_CONTENT)
async def remove_thread(thread_id: str, user_id: str = Depends(get_current_user)):
    success = await delete_thread(thread_id, user_id)
    if not success:
        raise HTTPException(status_code=404, detail="Thread not found or not authorized to delete")
    return {"message": "Thread deleted successfully"}

# Note: Implement the necessary CRUD operations in crud.py and update dependencies.py accordingly.
