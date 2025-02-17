import pandas as pd
import random
import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'
import pygame
from openai import OpenAI # type: ignore
from num2words import num2words

# Monster Info
ATTACK_MODIFIER = 3
DAMAGE_DICE = 6
DAMAGE_MODIFIER = 1

# Initialize
MODEL = "tts-1"
API_KEY = os.environ.get('OPENAI_API_KEY')
VOICE="ash"
pygame.mixer.init()

def dog_fight():
    players = pd.read_csv("players.csv")

    n = int(input("Input the number of hounds: "))

    # Make an array of who gets attacked
    number_of_players = len(players["Name"])
    attacks = [0] * number_of_players
    for _ in range(n):
        attacks[random.randint(0, number_of_players - 1)] += 1

    hits = [0] * number_of_players
    damages = [0] * number_of_players

    # Simulate the attacks
    for ii in range(number_of_players):
        for jj in range(attacks[ii]):
            # Roll the dice
            roll = random.randint(1, 20) + ATTACK_MODIFIER
            # Compare to the target player's AC
            if roll >= players[" AC"][ii]:
                hits[ii] += 1
                # Roll damage
                damages[ii] += random.randint(1, DAMAGE_DICE) + DAMAGE_MODIFIER
        
    print()
    print(attacks)
    print(hits)
    print(damages)
    print()

    # Announce the results
    for ii in range(number_of_players):
        announce(players["Name"][ii].strip(), attacks[ii], players[" Pronoun"][ii].strip(), damages[ii])

    dog_fight()

def announce(name: str, count: int, pronoun: str, damage: int):
    if not os.path.exists(f"dialogue\\{name}.mp3"):
        create_speech(name)
    play_sound(name)
    play_sound("was_attacked")
    if not os.path.exists(f"dialogue\\{count}.mp3"):
        create_number_speech(count)
    play_sound(str(count))
    if count == 1:
        play_sound("time")
    else:
        play_sound("times")
    if count == 0:
        return
    play_sound(pronoun)
    play_sound("took")
    if not os.path.exists(f"dialogue\\{damage}.mp3"):
        create_number_speech(damage)
    play_sound(str(damage))
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
    dog_fight()