from os import getenv
from dotenv import load_dotenv
from discord import Intents, Game
from asyncio import sleep
from aiohttp import ClientSession
from discord.ext import commands

from gas_price import fetch_estimates
from eth_price import fetch_eth_price

load_dotenv()
TOKEN = getenv('TOKEN')
TIMEOUT = 30
REST = 60

intents = Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

#---
@bot.command()
async def beth(ctx):
  while True:
    base, hi, mi, lo = fetch_estimates()
    fast, avrg, slow = list(map(lambda fee: round((fee + base)/10**9), [hi,mi,lo]))
    #fast, avrg, slow = [round((i + base)/10**9) for i in [hi,mi,lo]]
    usd = await fetch_eth_price()

    name = f'$ETH: {usd}✨'
    await ctx.guild.me.edit(nick=name)
    game = Game(f'🐇{fast} 🦊 {avrg} 🐢{slow}')
    await bot.change_presence(activity=game)
    await sleep(REST)

bot.run(TOKEN)
#-
