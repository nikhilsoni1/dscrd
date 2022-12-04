import random
import json
import requests
from pprint import pprint


def get_response(message: str) -> str:
    p_message = message.lower()

    if p_message == "hello":
        return "Hey there!"

    if message == "roll":
        return str(random.randint(1, 6))

    if p_message == "!help":
        return "`This is a help message that you can modify.`"
    
    if p_message == "!q":
        return get_quote()

    return 'I didn\'t understand what you wrote. Try typing "!help".'

def get_quote():
    response = requests.get("https://zenquotes.io/api/random")
    json_data = response.json()
    q = json_data[0]["q"]
    a = json_data[0]["a"]
    pld = f"{q} - {a}"
    return pld
