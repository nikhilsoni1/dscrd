import discord
import os
import requests
import pytz
import datetime
import emoji

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)


@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!"')
    channel = None
    channel = discord.utils.get(client.get_all_channels(), guild__name='East or west Shree is the Best!', name='daily-quotes')

    # cleaning up daily-quotes, messages not sent by this bot will be deleted
    messages = list()

    async for m in channel.history(limit=None):
        if m.author != client.user:
            messages.append(m)

    _now = discord.utils.utcnow()
    _delta = datetime.timedelta(days=14)
    _now_m14 = _now - _delta
    messages = list(filter(lambda x: x.created_at > _now_m14, messages))

    step = 100
    for m_d in discord.utils.as_chunks(messages, step):
        await channel.delete_messages(m_d, reason=f"{channel.name} clean-up, {client.user} messages kept intact.")
    
    title = emoji.emojize("Clean-up :broom: :broom:")
    footer = emoji.emojize("Swacch discord abhiyan :man_beard:")

    len_messages = len(messages)
    send_embed_flag = True
    if len_messages == 1:
        description = f"Deleted {len(messages)} message which wasn't a quote!"
    elif len_messages > 1:
        description = f"Deleted {len(messages)} messages which weren't quotes!"
    else:
        send_embed_flag = False

    footer = f"{footer}\nClean-ups occur regularly, messages which aren't quotes will be deleted."
    if send_embed_flag:
        embedVar = discord.Embed(title=title, description=description, color=discord.Color.red())
        embedVar.set_footer(text=footer)
        await channel.send(embed=embedVar)
    await client.close()


TOKEN = os.getenv("DISCORD_TOKEN")
client.run(TOKEN)
