import discord
import os
from collections import OrderedDict
import json
from tqdm import tqdm
import datetime

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)


@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!"')
    guild = os.getenv("DISCORD_GUILD")
    if guild == "soni's lab":
        pass
    else:
        await client.close()
    
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
    for channel in tqdm(channels):
        messages = list()
        async for m in channel.history(limit=None):
            messages.append(m)

        step = 100
        for m in discord.utils.as_chunks(messages, step):
            await channel.delete_messages(m, reason=f"{channel.name} clean-up")
    await client.close()

TOKEN = os.getenv("DISCORD_TOKEN")
client.run(TOKEN)