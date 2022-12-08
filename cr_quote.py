import discord
import os
import requests
import pytz

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)


@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!"')
    guild = os.getenv("DISCORD_GUILD")
    channel = None
    channel = discord.utils.get(
        client.get_all_channels(), guild__name=guild, name="daily-quotes"
    )

    u = discord.utils.utcnow()
    p = u.astimezone(tz=pytz.timezone("US/Pacific"))
    i = u.astimezone(tz=pytz.timezone("Asia/Kolkata"))
    e = u.astimezone(tz=pytz.timezone("US/East-Indiana"))
    pld = f"{u:%d %b %y %H:%M %Z}"
    if i.date() == e.date() == p.date():
        pld = f"{i:%d %b %y %H:%M %Z} - {e:%H:%M %Z} - {p:%H:%M %Z}"
    elif i.date() == e.date():
        pld = f"{i:%d %b %y %H:%M %Z} - {e:%H:%M %Z} | {p:%d %b %y %H:%M %Z}"
    elif e.date() == p.date():
        pld = f"{i:%d %b %y %H:%M %Z} | {e:%d %b %y %H:%M %Z} - {p:%H:%M %Z}"

    response = requests.get("https://zenquotes.io/api/random")
    json_data = response.json()
    q = json_data[0]["q"].strip()
    a = json_data[0]["a"].strip()
    q_t = f"\u200b\n{q}\n\u200b"
    embedVar = discord.Embed(color=discord.Color.random())
    embedVar.add_field(name=f"{a} says...", value=q_t)
    embedVar.set_footer(text=pld)

    await channel.send(embed=embedVar)
    await client.close()


TOKEN = os.getenv("DISCORD_TOKEN")
print(TOKEN)

client.run(TOKEN)

# Fetch a database of authors
# either fetch a random authors quote with image
# fetch a random quote
# credit zenquotes in footer
