import discord
from discord.ext import commands
# import responses
import os
import json
import random
import requests


TOKEN = os.getenv("DISCORD_TOKEN")
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)


@bot.event
async def on_ready():
    print(f"{bot.user.name} has connected to Discord!")


@bot.command(name="qb99", help="Responds with a random quote from Brooklyn 99")
async def nine_nine(ctx):
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


@bot.command(name="roll_dice", help="Simulates rolling dice.")
async def roll(ctx, number_of_dice=1, number_of_sides=6):
    d = range(1, number_of_sides+1)
    r = list()
    for i in range(number_of_dice):
        p = str(random.choice(d))
        r.append(p)
    if len(r) > 1:
        response = f"({', '.join(r)})"
    else:
        response = f"{r[0]}"
    print(response)
    await ctx.send(response)

@bot.command(name="q", help="Get a random quote from zenquotes.io")
async def get_quote(ctx):
    response = requests.get("https://zenquotes.io/api/random")
    json_data = response.json()
    q = json_data[0]["q"].strip()
    a = json_data[0]["a"].strip()
    embedVar = discord.Embed(title="says...", description=q, color=discord.Color.random())
    embedVar.set_author(name=a)
    await ctx.send(embed=embedVar)

bot.run(TOKEN)
