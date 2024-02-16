from typing import Union
from fastapi import FastAPI, Response
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from fastapi.responses import StreamingResponse
from dotenv import load_dotenv
from openai import OpenAI
from supabase import create_client, Client
import time
import json
import os

# Load the .env file
load_dotenv()

# Initialize Supabase client
supabase_url = os.getenv("SUPABASE_URL")
supabase_key = os.getenv("SUPABASE_KEY")
supabase: Client = create_client(supabase_url, supabase_key)

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

app = FastAPI(docs_url="/api/docs", openapi_url="/api/openapi.json")

@app.get("/api/healthchecker")
def healthchecker():
    return {"status": "success", "message": "Integrate FastAPI Framework with Next.js"}

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ChatCreate(BaseModel):
    prompt: str

# Define the ChatItem model
class ChatItem(BaseModel):
    id: int
    prompt: str
    reply: str

# In-memory storage for chat items
chats = []

def get_openai_stream(prompt: str):
    openai_stream = client.chat.completions.create(model="gpt-3.5-turbo-1106",
    messages=[{"role": "user", "content": prompt}],
    stream=True)
    try:
        for event in openai_stream:
            if event.choices[0].delta.content:
                current_response = event.choices[0].delta.content
                yield "data: " + current_response + "\n\n"
                time.sleep(0.1)
    except Exception as e:
        print("Stream encountered an error:", e)
    finally:
        yield "event: end-of-stream\ndata: \n\n"  # Signal the end of the stream


@app.get("/api/stream")
def stream(prompt: str):
    #response.headers['Cache-Control'] = 'no-cache'
    return StreamingResponse(get_openai_stream(prompt), media_type='text/event-stream')

# Route to get all chat items
@app.get("/api/chats")
async def get_all_chat_items():
    return chats