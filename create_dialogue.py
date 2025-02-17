import os
from openai import OpenAI # type: ignore

MODEL = "tts-1"
API_KEY = os.environ.get('OPENAI_API_KEY')
VOICE = "ash"

text = "resolve"
file_name = "Resolve"

client = OpenAI(api_key=API_KEY)
with client.audio.speech.with_streaming_response.create(
    model=MODEL,
    voice=VOICE,
    input=text
) as response:
    response.stream_to_file("dialogue\\" + file_name + ".mp3")