import discord
import os
from collections import OrderedDict
import json

# from pprint import pprint
from tqdm import tqdm
import datetime

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)


@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!"')
    guild = os.getenv("DISCORD_GUILD")
    channels = client.get_all_channels()
    channels = list(filter(lambda x: x.type.name == "text", channels))
    threads = list()
    for c in channels:
        c_thread = c.threads
        if len(c_thread) > 0:
            threads += c_thread
        else:
            pass
    channels = channels + threads
    store = list()
    for c in channels:
        pld = dict()
        pld.setdefault("guild_id", c.guild.id)
        pld.setdefault("guild_name", c.guild.name)
        pld.setdefault("channel_id", c.id)
        pld.setdefault("channel_name", c.name)
        pld.setdefault("channel_type", c.type.name)
        store.append(pld.copy())
    with open("dscrd-lab-channels.json", "w") as fp:
        json.dump(store, fp, indent=4)
    await client.close()


TOKEN = os.getenv("DISCORD_TOKEN")
client.run(TOKEN)
