from fastapi import APIRouter, Depends, HTTPException
from starlette.responses import StreamingResponse
from typing import List

from ..models import MessageCreate, MessageResponse  # Adjust import paths as needed
from ..crud import create_message, get_messages_for_thread  # Adjust import paths as needed
from ..openai_integration import generate_response  # Adjust import paths as needed
from ..dependencies import get_current_user  # Adjust import paths as needed

router = APIRouter()

@router.post("/threads/{thread_id}/messages/", response_model=MessageResponse)
async def send_message(thread_id: str, message: MessageCreate, user_id: str = Depends(get_current_user)):
    # Check if the message is intended for the chatbot
    if "<chatbot_identifier>" in message.content:  # Replace <chatbot_identifier> with your logic
        # Generate a response from OpenAI
        openai_response = generate_response(message.content)
        # Create a message in the database with OpenAI's response
        bot_response = await create_message(thread_id=thread_id, sender="<chatbot_name>", content=openai_response)
        return bot_response
    else:
        # Create a user message in the database
        user_message = await create_message(thread_id=thread_id, sender=user_id, content=message.content)
        return user_message

@router.get("/threads/{thread_id}/messages/", response_model=List[MessageResponse])
async def list_messages(thread_id: str):
    messages = await get_messages_for_thread(thread_id)
    if not messages:
        raise HTTPException(status_code=404, detail="No messages found in this thread")
    return messages

# Streaming endpoint for real-time chat updates
@router.get("/threads/{thread_id}/stream/")
async def stream_messages(thread_id: str):
    # Implement streaming logic here, potentially using WebSockets or Server-Sent Events (SSE)
    async def event_generator():
        # Dummy implementation - replace with real streaming logic
        while True:
            # Fetch new messages for the thread, e.g., those added since the last check
            new_messages = await get_messages_for_thread(thread_id)
            for message in new_messages:
                yield f"data: {message.json()}\n\n"
            await asyncio.sleep(1)  # Adjust the sleep time as needed

    return StreamingResponse(event_generator(), media_type="text/event-stream")
