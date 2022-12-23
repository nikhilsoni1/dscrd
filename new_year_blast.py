import discord
import os
import requests
import pytz
import json
from uuid import uuid4
import random

intents = discord.Intents.default()
intents.message_content = True
intents.members = True
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
        
        ord_f = "nayagan-nyeb-ord.json"
        with open(ord_f, "r") as fp:
            nyeb_order = json.load(fp)
    else:
        with open("dscrd-lab-channels.json", "r") as fp:
            channel_info = json.load(fp)

        with open("dscrd-lab-members.json", "r") as fp:
            member_info = json.load(fp)

        ord_f = "dscrd-lab-nyeb-ord.json"
        with open(ord_f, "r") as fp:
            nyeb_order = json.load(fp)

    nyeb_order_sorted = sorted(nyeb_order, key=lambda x: x["member_nyeb_order"])
    nyeb_order_filtered = list(filter(lambda x: not x["member_nyeb"], nyeb_order_sorted))
    if len(nyeb_order_filtered) == 0:
        await client.close()
        return None
    member = nyeb_order_filtered[0]
    member["member_nyeb"] = True
    member_id = member.get("member_id")
    member_mention = member.get("member_mention")
    
    _member = client.get_user(member_id)
    member_avatar = member.get("member_avatar")
    with open(ord_f, "w") as fp:
            nyeb_order = json.dump(nyeb_order_filtered, fp, indent=4, sort_keys=True)
    dm_title = "DM"
    dm_description = member.get("member_foo")
    embedVar = discord.Embed(title=dm_title, description=dm_description, color=discord.Color.random())
    # embedVar.set_thumbnail(url=member_avatar)
    await _member.send(embed=embedVar)

    # for c in channel_info:
    #     channel_id = c.get("channel_id")
    #     channel = client.get_channel(channel_id)
    #     channel_name = c.get("channel_name")
    #     gif = random.choice(gifs)
    #     title = f"Happy New Year 2023!"
    #     description = f"NYE DESCRIPTION {member_mention}"
    #     footer = f"NYE FOOTER\n{uuid4()}"
    #     embedVar = discord.Embed(
    #         title=title, description=description, color=discord.Color.random()
    #     )
    #     embedVar.set_image(url=gif)
    #     embedVar.set_footer(text=footer)
    #     print(f"{channel_name} - {footer}")
    #     await channel.send(embed=embedVar)
    await client.close()
    return None


TOKEN = os.getenv("DISCORD_TOKEN")
client.run(TOKEN)
