import discord
import os
from collections import OrderedDict
import json

# from pprint import pprint
from tqdm import tqdm
import datetime

intents = discord.Intents.default()
intents.message_content = True
intents.members = True
client = discord.Client(intents=intents)


@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!"')
    guild = os.getenv("DISCORD_GUILD")
    members = client.get_all_members()
    store = list()

    # for guild in client.guilds:
    #     for member in guild.members:
    #         foo = yield member
    #         print(foo.name)

    for m in members:
        if m.bot:
            continue
        pld = dict()
        pld.setdefault("member_id", m.id)
        pld.setdefault("member_mention", m.mention)
        pld.setdefault("member_avatar", m.avatar.url)
        pld.setdefault("member_name", m.name)
        pld.setdefault("member_discriminator", m.discriminator)
        store.append(pld.copy())
        print(f"{m.name}#{m.discriminator}")
    with open("dscrd-lab-members.json", "w") as fp:
        json.dump(store, fp, indent=4, sort_keys=True)
    await client.close()


TOKEN = os.getenv("DISCORD_TOKEN")
client.run(TOKEN)
