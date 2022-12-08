import discord
import os
import requests
import pytz
import datetime
import emoji
import random
from collections import OrderedDict
import json
from pprint import pprint
from tqdm import tqdm

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)
_FOO = None

@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!"')
    guild = os.getenv("DISCORD_GUILD")
    channels = client.get_all_channels()
    channels = list(filter(lambda x: x.type.name=="text", channels))
    threads = list()
    for c in channels:
        c_thread = c.threads
        if len(c_thread) > 0:
            threads += c_thread
        else:
            pass
    channels = channels + threads
    messages = list()
    for channel in tqdm(channels):
        async for m in channel.history(limit=None):
            messages.append(m)
    messages = list(filter(lambda x: x.author != client.user, messages))
    messages = list(filter(lambda x: len(x.embeds) > 0, messages))
    
    videos = list()
    for m in messages:

        sent_by = m.author.name
        in_channel = m.channel.name
        created_at = m.created_at

        any_video = False
        for e in m.embeds:
            if e.type == "video":
                title = e.title
                url = e.url
                video_info = OrderedDict()
                video_info.setdefault("title", title)
                video_info.setdefault("url", url)
                video_info.setdefault("sent_by", sent_by)
                video_info.setdefault("in_channel", in_channel)
                video_info.setdefault("created_at", created_at)
                videos.append(video_info.copy())
            else:
                debug = True
                pass
    with open("videos.json", "w") as fp:
        json.dump(obj=videos, fp=fp, indent=4, sort_keys=True, default=str, ensure_ascii=False)
    await client.close()
    debug = True
    


TOKEN = os.getenv("DISCORD_TOKEN")
client.run(TOKEN)
