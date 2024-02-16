from openai import OpenAI
import os
import time

# Assuming you've set your OpenAI API key in the environment variables
openai_api_key = os.getenv("OPENAI_API_KEY")
openai_client = OpenAI(api_key=openai_api_key)

def get_openai_stream(prompt: str):
    openai_stream = openai_client.chat.completions.create(
        model="gpt-3.5-turbo-1106",
        messages=[{"role": "user", "content": prompt}],
        stream=True
    )
    try:
        for event in openai_stream:
            if event.choices[0].delta.content:
                current_response = event.choices[0].delta.content
                yield "data: " + current_response + "\n\n"
                time.sleep(0.1)
    except Exception as e:
        print("Stream encountered an error:", e)
    finally:
        yield "event: end-of-stream\ndata: \n\n"
