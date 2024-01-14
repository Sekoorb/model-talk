from openai import OpenAI
from .config import settings

client = OpenAI(api_key=settings.openai_api_key)

def get_openai_stream(prompt: str):
    # ...
