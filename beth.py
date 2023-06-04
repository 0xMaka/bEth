from os import getenv
from dotenv import load_dotenv
from discord import Client, Intents, Status, Activity, ActivityType, Game
from asyncio import run, sleep
load_dotenv()

TOKEN = getenv('TOKEN')
#PERMS = getenv('PERMS')

#-----
from aiohttp import ClientSession
async def fetch_gas():
  async with ClientSession() as session:
    async with session.get('https://api.gasprice.io/v1/estimates',  timeout=5) as response:
      if response.status == 200:
        r = (await response.json())['result']
        return [r['instant']['feeCap'], r['fast']['feeCap'], r['eco']['feeCap'], r['ethPrice']]
      else:
        raise Exception(f'Call failed. Return code: {request.status}. \n')
#--

from discord.ext import commands
intents = Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.command()
async def beth(ctx):
  while True:
    hi, mi, lo, usd = await fetch_gas()
    name=f'$ETH: {usd}✨'
    await ctx.guild.me.edit(nick=name)
    game = Game(f'� {round(hi)} � {round(mi)} � {round(lo)}')
    await bot.change_presence(activity=game)
    await sleep(120)
