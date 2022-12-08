import discord
from discord.ext import commands

# import responses
import os
import json
import random
import requests


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

    ye_img = ["https://www.rollingstone.com/wp-content/uploads/2021/08/kanye-west-donda-review.jpg",
    "https://api.time.com/wp-content/uploads/2017/06/kanye-west-9.jpg",
    "https://i.guim.co.uk/img/static/sys-images/Guardian/Pix/pictures/2014/2/6/1391699663153/Kanye-West-and-Taylor-Swi-005.jpg",
    "https://www.highsnobiety.com/static-assets/thumbor/IN0vyfUCeBHGQlrKJZo3XjXpUCs=/1600x1067/www.highsnobiety.com/static-assets/wp-content/uploads/2022/10/21143756/demna-balenciaga-kanye-west-break-up-001.jpg",
    "https://media-cldnry.s-nbcnews.com/image/upload/newscms/2019_39/3029151/190927-kanye-west-ew-543p.jpg",
    "https://www.rollingstone.com/wp-content/uploads/2022/10/PiersKanye.jpg",
    "https://www.the-sun.com/wp-content/uploads/sites/6/2020/07/NINTCHDBPICT000596898568-10.jpg",
    "https://img.buzzfeed.com/buzzfeed-static/static/2021-08/24/15/enhanced/d5d4ff604871/original-1372-1629819648-12.jpg",
    "https://c8p9p3e5.rocketcdn.me/wp-content/uploads/2022/02/kanye-west-staring-meme.jpg",
    "https://hoopshype.com/wp-content/uploads/sites/92/2018/10/gettyimages-474901582.jpg"]

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
async def get_sweeper(ctx, limit: int=5):
    messages = list()
    async for m in ctx.channel.history(limit=limit):
        if m.author.bot != True:
            messages.append(m)
    step = 100
    for m in discord.utils.as_chunks(messages, step):
        await ctx.channel.delete_messages(m, reason=f"{ctx.channel.name} clean-up")

bot.run(TOKEN)
