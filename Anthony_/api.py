#import cv2
import urllib2
import numpy as np
import json

req = urllib2.urlopen('http://cs.mwsu.edu/~griffin/p-lot/apiproxy.php?time=1100')
req = ''.join(req)



def save(url):
    #url = "http://download.thinkbroadband.com/10MB.zip"
    file_name = url.split('/')[-1]
    u = urllib2.urlopen(url)
    in = open(file_name, 'wb')
    meta = u.info()
    file_size = int(meta.getheaders("Content-Length")[0])
    print "Downloading: %s Bytes: %s" % (file_name, file_size)

    file_size_dl = 0
    block_sz = 8192
    while True:
        buffer = u.read(block_sz)
        if not buffer:
            break

        file_size_dl += len(buffer)
        in.write(buffer)
        status = r"%10d  [%3.2f%%]" % (file_size_dl, file_size_dl * 100. / file_size)
        status = status + chr(8)*(len(status)+1)
        print status,

    in.close()


f = open("park.json", "w")

p_json = json.loads(req)
#json_data = json[49]
f.write(p_json)
f.close()

with open('park.json') as data_file:
    data = json.load(data_file)
#print (json_data)
for image in data['data']:
    url = image['shot_url']+image['camera']+'/'+image['name']
    print(url)
    req = urllib2.urlopen(url)
    save(url)
    arr = np.asarray(bytearray(req.read()), dtype=np.uint8)
    print(arr)
    #cv2.imshow('lalala',img)
    #if cv2.waitKey() & 0xff == 27: quit()