import cv2
import numpy as np
# original image
# -1 loads as-is so if it will be 3 or 4 channel as the original
image = cv2.imread('newspot.jpg', -1)

spots = [] #LIST OF SPOTS
#CREATES parkinglot array ->  need to find a correlation between spot points then do stuf in loops
for row in range (0,3):
    spots.append([])
    if(row == 0):
        #default starting spot cords for row 0 (x,y)
        topleft = [413,78]
        topright = [453,78]
        botleft = [419,115]
        botright = [463,115]
        row1topxints = [413,453,488,544,587,587]
        row1botxints = [419,463,498,559,610,610]
        ISIZE = 4
    if(row == 1):
        #default starting spot cords for row 1 (x,y)
        topleft = [37,174]
        topright = [76,172]
        botleft = [11,228]
        botright = [46,226]
        row1topxints= [37,76,115,149,193,238,283,330,378,424,467,514,538,538]
        row1botxints= [11,46,91,130,178,229,277,327,378,428,477,527,552,552]
        ISIZE = 12
    if(row == 2):
        #default starting spot cords for row 2 (x,y)
        topleft = [38,242]
        topright = [85,240]
        botleft = [0,312]
        botright = [54,310]
        row1topxints = [38,85,124,174,226,276,326,377,428,480,532,556,556]
        row1botxints = [0,54,100,155,215,270,324,377,433,493,549,574,574]
        ISIZE = 11
    for col in range(0,ISIZE):
        spots[row].append(col)
        mask = np.zeros(image.shape, dtype=np.uint8)
        roi_corners = np.array([[topleft, topright, botright,botleft]], dtype=np.int32)  # fill the ROI so it doesn't get wiped out when the mask is applied
        channel_count = image.shape[2]  # i.e. 3 or 4 depending on your image
        ignore_mask_color = (255,)*channel_count
        cv2.fillPoly(mask, roi_corners, ignore_mask_color)
        masked_image = cv2.bitwise_and(image, mask)  # apply the mask  


        topleft[1] = topright[1]
        topleft[0] = topright[0]
        topright[0] = row1topxints[col+2]
        if (row == 0):
            topright[1] = topright[1]
        else:
            topright[1] = topright[1] - 2


        botleft[0] = botright[0]
        botleft[1] = botright[1]
        botright[0] = row1botxints[col+2]
        if (row == 0):
             botright[1] = botright[1]
        else:
             botright[1] = botright[1] - 2
             
        print("TOP:" ,topright)
        print("BOT:", botright)

        newimg = 'Row_' + str(row) + ' Col_' + str(col)
        cv2.imwrite(newimg + '.jpg' , masked_image)