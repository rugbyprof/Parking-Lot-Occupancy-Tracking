import numpy as np
import cv2
import json


with open('parking.json') as data_file:
    data = json.load(data_file)
img = cv2.imread('Image2.jpg')

#JSON FILE NEEDS TO BE FIXED............
for row in range(0,3): #Change for how many spots
    if row == 0:
        ISIZE = 4
    if row == 1:
        ISIZE = 13
    if row == 2:
        ISIZE = 12
    for col in range (0,ISIZE):
        cv2.line(img,(int(data['Row'+str(row)+'_Col'+str(col)][0]['x']),int(data['Row'+str(row)+'_Col'+str(col)][0]['y'])), #1 -> 2
        (int(data['Row'+str(row)+'_Col'+str(col)][1]['x']),int(data['Row'+str(row)+'_Col'+str(col)][1]['y'])),(255,0,0),1)

        cv2.line(img,(int(data['Row'+str(row)+'_Col'+str(col)][0]['x']),int(data['Row'+str(row)+'_Col'+str(col)][0]['y'])), #1 -> 3
        (int(data['Row'+str(row)+'_Col'+str(col)][2]['x']),int(data['Row'+str(row)+'_Col'+str(col)][2]['y'])),(255,0,0),1)

        cv2.line(img,(int(data['Row'+str(row)+'_Col'+str(col)][1]['x']),int(data['Row'+str(row)+'_Col'+str(col)][1]['y'])), #2 -> 4
        (int(data['Row'+str(row)+'_Col'+str(col)][3]['x']),int(data['Row'+str(row)+'_Col'+str(col)][3]['y'])),(255,0,0),1)

        cv2.line(img,(int(data['Row'+str(row)+'_Col'+str(col)][2]['x']),int(data['Row'+str(row)+'_Col'+str(col)][2]['y'])), #3 -> 4
        (int(data['Row'+str(row)+'_Col'+str(col)][3]['x']),int(data['Row'+str(row)+'_Col'+str(col)][3]['y'])),(255,0,0),1)
cv2.imwrite("Test.jpg",img)