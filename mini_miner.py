import hashlib
import json
import os
from math import ceil

import requests
from dotenv import load_dotenv

load_dotenv()

access_token = os.environ.get('access_token')

get_url = f'https://hackattic.com/challenges/mini_miner/problem?access_token={access_token}'
post_url = f'https://hackattic.com/challenges/mini_miner/solve?access_token={access_token}'

data_to_unpack = json.loads(requests.get(get_url).text)
data_from_get = data_to_unpack['block']
difficulty = data_to_unpack['difficulty']

number_zeros = '0' * ceil(difficulty / 4)
solved = False
data_from_get['nonce'] = 0

while not solved:
    data_to_send = json.dumps(data_from_get, separators=(',', ':'), sort_keys=True)
    hash_from_data = hashlib.sha256(data_to_send.encode('utf-8'))
    if hash_from_data.hexdigest().startswith(number_zeros):
        solved = True
        solution_response = requests.post(post_url, data=json.dumps({'nonce': data_from_get['nonce']}))
        print(solution_response.text)
        print(hash_from_data.hexdigest())
    data_from_get['nonce'] += 1

