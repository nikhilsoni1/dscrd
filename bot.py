import discord
from discord.ext import commands
import re
import os
import json
import random
import requests
import asyncio
from uuid import uuid4


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
    d = range(1, number_of_sides + 1)
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
    embedVar = discord.Embed(
        title="says...", description=q, color=discord.Color.random()
    )
    embedVar.set_author(name=a)
    await ctx.send(embed=embedVar)


@bot.command(name="ye", help="Get a random quote from Ye a.k.a. Kanye West")
async def get_kanye(ctx):

    ye_img = [
        "https://www.rollingstone.com/wp-content/uploads/2021/08/kanye-west-donda-review.jpg",
        "https://api.time.com/wp-content/uploads/2017/06/kanye-west-9.jpg",
        "https://i.guim.co.uk/img/static/sys-images/Guardian/Pix/pictures/2014/2/6/1391699663153/Kanye-West-and-Taylor-Swi-005.jpg",
        "https://www.highsnobiety.com/static-assets/thumbor/IN0vyfUCeBHGQlrKJZo3XjXpUCs=/1600x1067/www.highsnobiety.com/static-assets/wp-content/uploads/2022/10/21143756/demna-balenciaga-kanye-west-break-up-001.jpg",
        "https://media-cldnry.s-nbcnews.com/image/upload/newscms/2019_39/3029151/190927-kanye-west-ew-543p.jpg",
        "https://www.rollingstone.com/wp-content/uploads/2022/10/PiersKanye.jpg",
        "https://www.the-sun.com/wp-content/uploads/sites/6/2020/07/NINTCHDBPICT000596898568-10.jpg",
        "https://img.buzzfeed.com/buzzfeed-static/static/2021-08/24/15/enhanced/d5d4ff604871/original-1372-1629819648-12.jpg",
        "https://c8p9p3e5.rocketcdn.me/wp-content/uploads/2022/02/kanye-west-staring-meme.jpg",
        "https://hoopshype.com/wp-content/uploads/sites/92/2018/10/gettyimages-474901582.jpg",
    ]

    ye_img = random.choice(ye_img)
    response = requests.get("https://api.kanye.rest")
    j = response.json()
    q = j.get("quote")
    if q is not None:
        q = q.strip()
    a = f"Ye a.k.a. Kanye West says..."
    embedVar = discord.Embed(title=q, color=discord.Color.random())
    embedVar.set_image(url=ye_img)
    embedVar.set_author(name=a)
    await ctx.send(embed=embedVar)


@bot.command(name="sweep", help="Sweep last n messages not posted by a bot")
async def get_sweeper(ctx, limit: int = 5):
    messages = list()
    async for m in ctx.channel.history(limit=limit):
        if m.author.bot != True:
            messages.append(m)
    step = 100
    for m in discord.utils.as_chunks(messages, step):
        await ctx.channel.delete_messages(m, reason=f"{ctx.channel.name} clean-up")


@bot.command(name="s60", help="Get a random quote from Ye a.k.a. Kanye West")
async def get_s60(ctx):

    with open("s60_quotes.json", "r") as fp:
        quotes = json.load(fp)
    q = random.choice(quotes).strip()
    q = re.sub("\n{1,10}", "\n\n", q)
    q = f"{q}\n"
    title = "Studio 60 on the Sunset Strip"
    embedVar = discord.Embed(title=title, description=q, color=discord.Color.random())
    await ctx.send(embed=embedVar)

@bot.command(name="bb", help="Boombastic")
async def get_bb(ctx, winner: discord.User=None):
    winning_user_name = winner.name
    # return None
    current_channel_id = ctx.channel.id
    current_channel = bot.get_channel(current_channel_id)
    dumbledore_clapping = discord.Embed(color=discord.Color.random())
    dumbledore_clapping.set_image(
        url="https://media.tenor.com/iQfqZ-n4QDgAAAAC/dumbledore-applause.gif"
    )

    obama_t = f"{winning_user_name} wins the 1st Hangman Triward Tournament"
    obama_d = "suck it up losers..."
    obama_out = discord.Embed(title=obama_t, description=obama_d, color=discord.Color.dark_gold())
    obama_out.set_image(url="https://media.tenor.com/WJIEOHsnJmkAAAAC/obama-mic-drop.gif")

    with open("tenor-search-for-term-winner.json", "r") as fp:
        winner_gifs = json.load(fp)

    which_guild = os.getenv("DISCORD_GUILD")

    if which_guild == "East or west Shree is the Best!":
        with open("nayagan-channels.json", "r") as fp:
            channel_info = json.load(fp)
    else:
        with open("dscrd-lab-channels.json", "r") as fp:
            channel_info = json.load(fp)
            
    channel_info = list(filter(lambda x: x.get("channel_id") != current_channel_id, channel_info))
    dumbledore_message = await ctx.send(embed=dumbledore_clapping)

    countdown_gifs = [
        "https://media.tenor.com/oRFRlKfQtHwAAAAC/fist-fight-ice-cube.gif",
        "https://media.tenor.com/cpQa4b7u5voAAAAM/cubs-two.gif",
        "https://media.tenor.com/R13zRSd25owAAAAC/number1-numberone.gif",
        "https://media.tenor.com/WRFJ3pkp_9IAAAAC/los-angeles-lakers-lebron-james.gif"

    ]

    countdown_messages = list()
    countdown_messages.append(dumbledore_message)
    await asyncio.sleep(3)
    for c_gif in countdown_gifs:
        footer = f"{uuid4()}"
        print(f"countdown - {footer}")
        embd = discord.Embed(color=discord.Color.dark_gold())
        embd.set_image(url=c_gif)
        embd.set_footer(text=footer)
        m = await ctx.send(embed=embd)
        await asyncio.sleep(3)
        countdown_messages.append(m)

    # Server blast
    for channel in channel_info:
        await asyncio.sleep(1)
        channel_id = channel.get("channel_id")
        c = bot.get_channel(channel_id)
        n = channel.get("channel_name")
        d = uuid4()
        g = random.choice(winner_gifs)
        embed_t = f"{winning_user_name} wins the 1st Hangman Triward Tournament"
        embed_d = "suck it up losers..."
        embedVar = discord.Embed(title=embed_t, description=embed_d, color=discord.Color.random())
        embedVar.set_image(url=g)
        embedVar.set_footer(text=d)
        print(f"{n} - {d}")
        await c.send(embed=embedVar)
    print(f"{'-'*20}\n")

    await current_channel.delete_messages(countdown_messages)
    await ctx.send(content = "@everyone")
    await asyncio.sleep(3)
    await ctx.send(embed=obama_out)

bot.run(TOKEN)
