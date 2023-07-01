from web3 import Web3
from functools import reduce

from os import getenv
from dotenv import load_dotenv
load_dotenv()

w3 = Web3(Web3.HTTPProvider(getenv(ENDPOINT)))

def format_fee_history(result, include_pending):
  block_num = result.oldestBlock
  index = 0
  blocks = []
  pending_base_fee = result.baseFeePerGas.pop()
  while block_num < result.oldestBlock + len(result.reward):
    blocks.append(
      {
        'number': block_num,
        'baseFeePerGas': result.baseFeePerGas[index],
        'gasUsedRatio': result.gasUsedRatio[index],
        'priorityFeePerGas': result.reward[index]
      }
    )
    block_num += 1
    index += 1
    if include_pending:
      blocks.append(
        {
          'number': 'pending',
          'baseFeePerGas': pending_base_fee,
          'gasUsedRatio':  None,
          'priorityFeePerGas': []
        }
      )
  return blocks

def fetch_estimates():
  fee_history = w3.eth.fee_history(20,'pending',[20,50,80])
  blocks = format_fee_history(fee_history, False)

  hi = list(map(lambda b: b['priorityFeePerGas'][2], blocks))
  mi = list(map(lambda b: b['priorityFeePerGas'][1], blocks))
  lo = list(map(lambda b: b['priorityFeePerGas'][0], blocks))
  
  estimates = []
  estimates.append(w3.eth.get_block('pending').baseFeePerGas)
  for items in [hi, mi, lo]:
    estimates.append(round(reduce(lambda a, v: a + v, items)/len(items)))

  return estimates

if __name__ == '__main__':  
  base, high, medium, low = fetch_estimates()
  print('max :',w3.eth.max_priority_fee + base)
  print('high:',high + base)
  print('mid :',medium + base)
  print('low :',low + base)
