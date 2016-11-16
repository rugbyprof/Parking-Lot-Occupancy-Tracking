import cv2
import urllib2
import numpy as np
import json

req = urllib2.urlopen('http://cs.mwsu.edu/~griffin/p-lot/apiproxy.php?time=1100')
req = ''.join(req)
f = open("Park.json", "w")
p_json = json.loads(req)
f.write(p_json)
f.close()
with open('park.json') as data_file:
        data = json.load(data_file)
for image in data['data']:
    print(image['shot_url']+image['camera']+'/'+image['name'])
    req = urllib2.urlopen(image['shot_url']+image['camera']+'/'+image['name'])
    arr = np.asarray(bytearray(req.read()), dtype=np.uint8)
    print(arr)
    #cv2.imshow('lalala',img)
    #if cv2.waitKey() & 0xff == 27: quit()