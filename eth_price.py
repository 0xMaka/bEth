from asyncio import run
from aiohttp import ClientSession
TIMEOUT = 10

async def fetch_price_from_sushi():
  async with ClientSession() as session:
    async with session.post('https://api.thegraph.com/subgraphs/name/sushiswap/exchange', json={'query': '{bundle(id: 1) {ethPrice}}'}, timeout=TIMEOUT) as response:
      if response.status == 200:
        price = await response.json()
        return round(float(price['data']['bundle']['ethPrice']),2)
      else:
        raise Exception(f'Call failed. Return code: {response.status}. \n')

async def fetch_eth_price():
  price = await fetch_price_from_sushi()
  if not price:
    return 0
  else:
    return price

if __name__ == '__main__':
  print(f'[+] Result: {run(fetch_eth_price())}')
