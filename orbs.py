import pandas as pd
import random
import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'
import pygame
from openai import OpenAI # type: ignore
from num2words import num2words

# Initialize
players = pd.read_csv("players.csv")
MODEL = "tts-1"
API_KEY = os.environ.get('OPENAI_API_KEY')
VOICE="ash"
pygame.mixer.init()

def orb():
    n = int(input("Input orb_damage: "))

    # Distribute damage evenly
    number_of_players = len(players["Name"])
    attacks = [0] * number_of_players
    for _ in range(n):
        attacks[random.randint(0, number_of_players - 1)] += 1
        
    print()
    print(attacks)
    print()

    # Announce the results
    for ii in range(number_of_players):
        announce(players["Name"][ii].strip(), attacks[ii])

    orb()

def announce(name: str, count: int):
    if not os.path.exists(f"dialogue\\{name}.mp3"):
        create_speech(name)
    play_sound(name)
    play_sound("took")
    if not os.path.exists(f"dialogue\\{count}.mp3"):
        create_number_speech(count)
    play_sound(str(count))
    play_sound("damage")

def play_sound(file: str):
    pygame.mixer.music.load(f"dialogue\\{file}.mp3")
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():  # Keep script running while music is playing
        pass

def create_speech(text: str):
    client = OpenAI(api_key=API_KEY)
    with client.audio.speech.with_streaming_response.create(
        model=MODEL,
        voice=VOICE,    
        input=text
    ) as response:
        response.stream_to_file(f"dialogue\\{text}.mp3")     

def create_number_speech(num: int):
    text = num2words(num)
    client = OpenAI(api_key=API_KEY)
    with client.audio.speech.with_streaming_response.create(
        model=MODEL,
        voice=VOICE,    
        input=text
    ) as response:
        response.stream_to_file(f"dialogue\\{num}.mp3")   

if __name__ == "__main__":
    orb()