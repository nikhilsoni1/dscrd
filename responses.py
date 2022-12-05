import random
import json
import requests
from pprint import pprint
import discord


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

    if p_message == "!qb99":
        return get_b99()
        

    return None

def get_quote():
    response = requests.get("https://zenquotes.io/api/random")
    json_data = response.json()
    q = json_data[0]["q"]
    a = json_data[0]["a"]
    pld = f"{q} - {a}"
    return pld

def get_b99():
    with open("b99.json", "r") as stream:
        _root = json.load(stream)
    j = _root.get("root")
    q = random.choice(j)
    c = q.get("Character")
    h = q.get("Header")
    e = q.get("Episode")
    t = q.get("QuoteText")

    t_t = t.replace(". ", ".\n\n")
    embedVar = discord.Embed(title=h, description=t_t, type="rich")
    await ctx.send(embed=embedVar)
    return fq
