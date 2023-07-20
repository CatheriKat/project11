import random
import time

import eth_utils
import requests
from web3 import Account

Account.enable_unaudited_hdwallet_features()
with open('bip39-en.txt', 'r') as words_file:
    words = [word.removesuffix('\n') for word in words_file.readlines()]

c = 0
addys = []
phrases = []

phrases = {}
while True:

    phrase = ' '.join(random.sample(words, 12)).strip()

    try:
        acc = Account.from_mnemonic(phrase)
    except eth_utils.exceptions.ValidationError:
        continue

    phrases[str(acc.address).lower()] = phrase

    random_head = f'{{"random_at":1680433644,"random_id":"cd2830e4443f4222a29c9368853de4b8",' \
                  f'"session_id":"98c442a47c894b2fb076c2ca5015a991",' \
                  f'"user_addr":"{acc.address}","wallet_type":"metamask","is_verified":false}}'

    headers = {
        "sec-ch-ua": f"\"Google Chrome\";v=\"107\", \"Chromium\";v=\"10{random.randint(6, 9)}\", \"Not=A?Brand\";v=\"24\"",
        "x-api-sign": "ae276b6262ed4482cd6bfde360afcefc9dfb6b55e9d95c31290cfa31f6320545",
        "account": random_head,
        "source": "web",
        "sec-ch-ua-mobile": "?0",
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36",
        "x-api-ts": "1680983629",
        "x-api-ver": "v2",
        "x-api-nonce": "n_czcSQOBt7ssryo9k4Xzt8eSL9WvsTyQqf1MGo6WF",
        "sec-ch-ua-platform": "\"Windows\"",
        "Accept": "*/*",
        "host": "api.debank.com"
    }

    if len(phrases) > 80:
      addys = [i for i in phrases]
      c += 1
      print(c)
      url = 'https://api.debank.com/user/desc_dict?ids='
      url += ','.join(addys)
      try:
          response = requests.get(f'{url}', headers=headers)
      except:
          time.sleep(180)
          response = requests.get(f'{url}', headers=headers)
      for wallet, data in response.json().get('data').get('desc_dict').items():
          if (data.get('born_at') is not None) or data.get('usd_value') > 0:
              print(wallet, data.get('born_at'), data.get('usd_value'), phrases[wallet])
              with open(f'find{acc.address}.txt', 'w') as f:
                  f.write(f"{wallet}, {data.get('born_at')}, {data.get('usd_value')}, {phrases[wallet]}")
                  f.close()

      addys = []
      phrases = {}
      #print(c)
      time.sleep(20)
