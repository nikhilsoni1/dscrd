import discord
import os
import requests
import pytz
import json
from uuid import uuid4
import random

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)


@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!"')
    guild = os.getenv("DISCORD_GUILD")

    with open("tenor-search-for-term-nye.json", "r") as fp:
        gifs = json.load(fp)

    if guild == "East or west Shree is the Best!":
        with open("nayagan-channels.json", "r") as fp:
            channel_info = json.load(fp)

        with open("nayagan-members.json", "r") as fp:
            member_info = json.load(fp)
    else:
        with open("dscrd-lab-channels.json", "r") as fp:
            channel_info = json.load(fp)

        with open("dscrd-lab-members.json", "r") as fp:
            member_info = json.load(fp)

    for c in channel_info:
        channel_id = c.get("channel_id")
        channel = client.get_channel(channel_id)
        channel_name = c.get("channel_name")
        gif = random.choice(gifs)
        title = f"Happy New Year 2023!"
        description = "NYE DESCRIPTION"
        footer = f"NYE FOOTER\n{uuid4()}"
        embedVar = discord.Embed(
            title=title, description=description, color=discord.Color.random()
        )
        embedVar.set_image(url=gif)
        embedVar.set_footer(text=footer)
        print(f"{channel_name} - {footer}")
        await channel.send(embed=embedVar)
    await client.close()
    return None


TOKEN = os.getenv("DISCORD_TOKEN")
client.run(TOKEN)
