import os
from dotenv import load_dotenv

load_dotenv()
import requests
import base64
import json
from struct import unpack

access_token = os.environ.get('access_token')

get_url = f'https://hackattic.com/challenges/help_me_unpack/problem?access_token={access_token}'
post_url = f'https://hackattic.com//challenges/help_me_unpack/solve?access_token={access_token}'
data_to_unpack = json.loads(requests.get(get_url).text)

bytes_to_decode = data_to_unpack['bytes']
bytes_decoded = base64.standard_b64decode(bytes_to_decode)

int_value = unpack('<i', bytes_decoded[:4])[0]
uint_value = unpack('<I', bytes_decoded[4:8])[0]
short_value = unpack('<h', bytes_decoded[8:10])[0]
float_value = unpack('<f', bytes_decoded[12:16])[0]
double_value = unpack('<d', bytes_decoded[16:24])[0]
big_endian = unpack('>d', bytes_decoded[24:32])[0]

solution = {'int': int_value, 'uint': uint_value, 'short': short_value, 'float': float_value, 'double': double_value, 'big_endian_double': big_endian}

solution_response = requests.post(post_url, data=json.dumps(solution))
print(solution_response.text)
