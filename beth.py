from os import getenv
from dotenv import load_dotenv
from discord import Intents, Game
from asyncio import run, sleep
from aiohttp import ClientSession
from discord.ext import commands

load_dotenv()
TOKEN = getenv('TOKEN')
TIMEOUT = 5
REST = 60

intents = Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

#---

async def fetch_prices():
  async with ClientSession() as session:
    async with session.get('https://api.gasprice.io/v1/estimates',  timeout=TIMEOUT) as response:
      if response.status == 200:
        r = (await response.json())['result']
        return [r['instant']['feeCap'], r['fast']['feeCap'], r['eco']['feeCap'], r['ethPrice']]
      else:
        raise Exception(f'Call failed. Return code: {request.status}. \n')
#--

@bot.command()
async def beth(ctx):
  while True:
    hi, mi, lo, usd = await fetch_prices()
    name=f'$ETH: {usd}✨'
    await ctx.guild.me.edit(nick=name)
    game = Game(f'� {round(hi)} � {round(mi)} � {round(lo)}')
    await bot.change_presence(activity=game)
    await sleep(REST)

bot.run(TOKEN)
#-
