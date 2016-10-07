import numpy as np
import cv2
import json

def cutParkingSpot(img, points, idx):
    parkingSpot = img[int(points[0]['y']):int(points[3]['y']), int(points[0]['x']):int(points[3]['x'])]
    new_p_spot = img[int(points[0]['y']):int(points[3]['y']), int(points[0]['x']):int(points[3]['x'])]
    width, height = img.shape[:2]
    print width, height
    res = cv2.resize(parkingSpot, (width/3, height/3), cv2.INTER_LANCZOS4)
    cv2.imshow("spot created", res)
    cv2.imwrite('spot'+str(idx)+'.jpg',res)
    #cv2.imshow("m", img)
    cv2.waitKey(0)
    return

with open('newParking.json') as data_file:
    data = json.load(data_file)

# Create a black image
#img = np.zeros((512,512,3), np.uint8)
img = cv2.imread('img.jpg')

# Draw a diagonal blue line with thickness of 5 px
#cv2.line(img,(0,0),(511,511),(255,0,0),1)

# for letter,points in data.items():
#     print(points[0])
#     print(points[1])
#
#     cv2.line(img,(int(points[0]['x']),int(points[0]['y'])),(int(points[1]['x']),int(points[1]['y'])),(255,0,0),1)

for i in range(0,5):
    print(chr(65+i))
    cv2.line(img,(int(data[chr(65+i)][0]['x']),int(data[chr(65+i)][0]['y'])),(int(data[chr(65+i)][1]['x']),int(data[chr(65+i)][1]['y']))
,(255,0,0),1)
    cv2.line(img,(int(data[chr(65+i)][0]['x']),int(data[chr(65+i)][0]['y'])),(int(data[chr(65+i)][2]['x']),int(data[chr(65+i)][2]['y']))
,(255,0,0),1)
    cv2.line(img,(int(data[chr(65+i)][1]['x']),int(data[chr(65+i)][1]['y'])),(int(data[chr(65+i)][3]['x']),int(data[chr(65+i)][3]['y']))
,(255,0,0),1)
    cv2.line(img,(int(data[chr(65+i)][2]['x']),int(data[chr(65+i)][2]['y'])),(int(data[chr(65+i)][3]['x']),int(data[chr(65+i)][3]['y']))
,(255,0,0),1)
    cutParkingSpot(img, data[chr(65+i)], i)

# i = 7
# print(chr(65+i))
#
# cv2.line(img,(int(data[chr(65+i)][0]['x']),int(data[chr(65+i)][0]['y'])),(int(data[chr(65+i)][1]['x']),int(data[chr(65+i)][1]['y'])),(
#255,0,0),1)

cv2.imwrite('out.jpg',img)
#cutParkingSpot(img)

