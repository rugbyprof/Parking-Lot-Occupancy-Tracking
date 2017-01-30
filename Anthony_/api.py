#import cv2
import urllib2
import numpy as np
import json

req = urllib2.urlopen('http://cs.mwsu.edu/~griffin/p-lot/apiproxy.php?dayOfYear=256')
req = ''.join(req)

f = open("park.json", "w")

p_json = json.loads(req)
#json_data = json[49]
f.write(p_json)
f.close()

with open('park.json') as data_file:
    data = json.load(data_file)
#print (json_data)
for image in data['data']:
    #url = image['shot_url']+image['camera']+'/'+image['name']
    #print(url)
    #req = urllib2.urlopen(url)
    #save(url)
    #arr = np.asarray(bytearray(req.read()), dtype=np.uint8)
    #print(arr)
    #cv2.imshow('lalala',img)
    #if cv2.waitKey() & 0xff == 27: quit()
    print(1)