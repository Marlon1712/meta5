from ppadb.client import Client
from PIL import Image
import numpy as np
# import tratamento

import time

adb = Client(host='127.0.0.1', port=5037)
devices = adb.devices()

if len(devices) == 0:
    print('no device attached')
    quit()

device = devices[0]

# image = device.screencap()

# with open('screen.png','wb') as f:
#     f.write(image)
# image = Image.open('screen.png')
# #image = np.array(image, dtype=np.uint8)
# image_crop = image.crop((70,650,1010,1580))
# image_crop.save('image_crop.png')
# pos = np.array([[130,715], [275,715], [400,715], [535,715], [675,715], [805,715], [945,715]])

# tratamento.main()

# r = '450 1775'
# g = '625 1775'
# b = '280 1775'
# o = '825 1775'
# comannd = f'input touchscreen tap {g}'
# device.shell(comannd)

n = '550 2272'
j = '550 2048'
c = '542 1896'

x = 0
while x < 100:
    print(f'execucao n: {x + 1}') 
    comannd = f'input touchscreen tap {c}'
    device.shell(comannd)
    time.sleep(0.5)
    comannd = f'input touchscreen tap {n}'
    device.shell(comannd)
    time.sleep(8)
    x += 1