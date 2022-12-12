import discord
import os

# import requests
# import pytz
# import datetime
# import emoji
# import random
from collections import OrderedDict
import json

# from pprint import pprint
from tqdm import tqdm
import datetime

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

json_store = "yt_info"
run_info_file = os.path.join(json_store, "run_info.txt")
os.makedirs("yt_info", exist_ok=True)

run_info_exists = os.path.exists(run_info_file)


ts = discord.utils.utcnow()

if run_info_exists:
    with open(run_info_file, "r") as fp:
        run_history = fp.readlines()
        latest = run_history[-1].strip()
        latest_ts = datetime.datetime.fromisoformat(latest)
        debug = True
else:
    ts_floor = ts.replace(hour=0, minute=0, second=0, microsecond=0)
    ts_floor_m7d = ts_floor - datetime.timedelta(days=7)
    latest_ts = ts_floor_m7d


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
    messages = list()
    for channel in tqdm(channels):
        async for m in channel.history(after=latest_ts):
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
    output_file_name = f"yt-{ts:%Y-%m-%d-%H-%M-%S-%f}.json"
    fpath = os.path.join(json_store, output_file_name)
    if len(videos) > 0:
        with open(fpath, "w") as fp:
            json.dump(
                obj=videos,
                fp=fp,
                indent=4,
                sort_keys=True,
                default=str,
                ensure_ascii=False,
            )
    else:
        pass
    await client.close()


TOKEN = os.getenv("DISCORD_TOKEN")
client.run(TOKEN)
with open(run_info_file, "w") as fp:
    fp.write(f"{ts}\n")
