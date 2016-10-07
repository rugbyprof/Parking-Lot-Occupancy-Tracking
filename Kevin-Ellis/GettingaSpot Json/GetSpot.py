import cv2
import json
import numpy as np
from matplotlib import pyplot as plt   
# original image
# -1 loads as-is so if it will be 3 or 4 channel as the original
image = cv2.imread('image2.jpg', -1)
with open('parking.json') as data_file:
    data = json.load(data_file)

def getmin(p1,p2,p3,p4):
    minx =  min(p1[0],p2[0],p3[0],p4[0])
    miny =  min(p1[1],p2[1],p3[1],p4[1])
    return(minx,miny)
def getmax(p1,p2,p3,p4):
    maxx =  max(p1[0],p2[0],p3[0],p4[0])
    maxy =  max(p1[1],p2[1],p3[1],p4[1])
    return(maxx,maxy)
def histogram(image):
    # grab the image channels, initialize the tuple of colors,
    # the figure and the flattened feature vector
    chans = cv2.split(image)
    colors = ("b", "g", "r")
    plt.figure()
    plt.title("'Flattened' Color Histogram")
    plt.xlabel("Bins")
    plt.ylabel("# of Pixels")
    features = []
 
    # loop over the image channels
    for (chan, color) in zip(chans, colors):
        # create a histogram for the current channel and
        # concatenate the resulting histograms for each
        # channel
        hist = cv2.calcHist([chan], [0], None, [256], [0, 256])
        features.extend(hist)
    
        # plot the histogram
        plt.plot(hist, color = color)
        plt.xlim([0, 256])
    
    # here we are simply showing the dimensionality of the
    # flattened color histogram 256 bins for each channel
    # x 3 channels = 768 total values -- in practice, we would
    # normally not use 256 bins for each channel, a choice
    # between 32-96 bins are normally used, but this tends
    # to be application dependent
    print "flattened feature vector size: %d" % (np.array(features).flatten().shape)
    plt.show()  


for row in range (0,3):
    if row == 0:
        ISIZE = 4
    if row == 1:
        ISIZE = 13
    if row == 2:
        ISIZE = 12
    for col in range (0,ISIZE):
        topleft = (int(data['Row'+str(row)+'_Col'+str(col)][0]['x']) , int(data['Row'+str(row)+'_Col'+str(col)][0]['y']))
        topright = (int(data['Row'+str(row)+'_Col'+str(col)][1]['x']) , int(data['Row'+str(row)+'_Col'+str(col)][1]['y']))
        botleft = (int(data['Row'+str(row)+'_Col'+str(col)][2]['x']) , int(data['Row'+str(row)+'_Col'+str(col)][2]['y']))
        botright= (int(data['Row'+str(row)+'_Col'+str(col)][3]['x']) , int(data['Row'+str(row)+'_Col'+str(col)][3]['y']))
        mask = np.zeros(image.shape, dtype=np.uint8)
        roi_corners = np.array([[topleft, topright, botright,botleft]], dtype=np.int32)  # fill the ROI so it doesn't get wiped out when the mask is applied
        channel_count = image.shape[2]  # i.e. 3 or 4 depending on your image
        ignore_mask_color = (255,)*channel_count
        cv2.fillPoly(mask, roi_corners, ignore_mask_color)
        masked_image = cv2.bitwise_and(image, mask)  # apply the mask 

        minpoint = getmin(topleft,topright,botleft,botright)
        maxpoint = getmax(topleft,topright,botleft,botright)

        spot = masked_image[minpoint[1]:maxpoint[1], minpoint[0]:maxpoint[0]]
        histogram(spot)

        newimg = 'Row_' + str(row) + ' Col_' + str(col)
        cv2.imwrite(newimg + '.jpg' , spot)
