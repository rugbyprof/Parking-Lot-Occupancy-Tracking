import cv2
import os
import json
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mpimg

def resizeimage(orgimage):
    resized_image = cv2.resize(orgimage, (640, 480)) 
    return (resized_image)
def getmin(p1,p2,p3,p4):
    minx =  min(p1[0],p2[0],p3[0],p4[0])
    miny =  min(p1[1],p2[1],p3[1],p4[1])
    return(minx,miny)
def getmax(p1,p2,p3,p4):
    maxx =  max(p1[0],p2[0],p3[0],p4[0])
    maxy =  max(p1[1],p2[1],p3[1],p4[1])
    return(maxx,maxy)
def histogram(image,newimg):
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
    dirname = 'Histograms'
    plt.savefig(os.path.join(dirname, newimg +  'Hist' + '.png'))
    plt.close()
def comparehist():
    hist1 = mpimg.imread("Row_1 Col_12Hist.png")
    hist2 = mpimg.imread("Row_2 Col_11Hist.png")

    Correlation = cv2.compareHist(hist1,hist2,method=cv2.HISTCMP_CORREL)
    ChiSquare = cv2.compareHist(hist1,hist2,method=cv2.HISTCMP_CHISQR)
    Intersection = cv2.compareHist(hist1,hist2,method=cv2.HISTCMP_INTERSECT)
    BhattacharyyaDistance = cv2.compareHist(hist1,hist2,method=cv2.HISTCMP_BHATTACHARYYA)
    Hellinger = cv2.compareHist(hist1,hist2,method=cv2.HISTCMP_HELLINGER)

    print('Correlation:', Correlation)
    print('Chi Square:', ChiSquare)
    print('Intersection:', Intersection)
    print('Bhattacharyya Distance:', BhattacharyyaDistance)
    print('Hellinger:', Hellinger )

def getxval(num):
    xval = int(data['Row'+str(row)+'_Col'+str(col)][num]['x'])
    return (xval)
def getyval(num):
    yval = int(data['Row'+str(row)+'_Col'+str(col)][num]['y'])
    return (yval)
def drawline(topleft,topright,botright,botleft,img):
    cv2.line(img,(topleft[0],topleft[1]),(topright[0],topright[1]),(255,0,0),1)#1 -> 2
    cv2.line(img,(topleft[0],topleft[1]),(botleft[0],botleft[1]),(255,0,0),1) #1 -> 3
    cv2.line(img,(topright[0],topright[1]),(botright[0],botright[1]),(255,0,0),1) #2 -> 4
    cv2.line(img,(botleft[0],botleft[1]),(botright[0],botright[1]),(255,0,0),1) #3 -> 4
    cv2.imwrite("Lines.jpg",img)

def makenewimage(newimg,spot):
    dirname = 'Spots'
    res = cv2.resize(spot,(50, 70))
    cv2.imwrite(os.path.join(dirname, newimg + '.jpg'), res)
def makegreyscaleimage(newimg,spot):
    greydirname = 'Spots-Grey'
    res = cv2.resize(spot,(50, 70))
    gray_image = cv2.cvtColor(res, cv2.COLOR_BGR2GRAY)
    cv2.imwrite(os.path.join(greydirname, newimg + '.jpg'),gray_image)
def maskimage(topleft,topright,botright,botleft):
    mask = np.zeros(image.shape, dtype=np.uint8)
    roi_corners = np.array([[topleft, topright, botright,botleft]], dtype=np.int32)  # fill the ROI so it doesn't get wiped out when the mask is applied
    channel_count = image.shape[2]  # i.e. 3 or 4 depending on your image
    ignore_mask_color = (255,)*channel_count
    cv2.fillPoly(mask, roi_corners, ignore_mask_color)
    masked_image = cv2.bitwise_and(image, mask)  # apply the mask
    return(masked_image)



if __name__ == "__main__":
    image = cv2.imread('image2.jpg', -1)
    image = cv2.resize(image,(640,480))
    with open('parking.json') as data_file:
        data = json.load(data_file)
    for row in range (0,3):#0 -> number of rows of spots [fix with griffin's json]
        if row == 0:
            numspots = 4
        if row == 1:
            numspots = 13
        if row == 2:
            numspots= 12
        for col in range (0,numspots): #0 -> number of spots in a row
            newimg = 'Row_' + str(row) + ' Col_' + str(col)
            topleft = (getxval(0) , getyval(0))
            topright = (getxval(1) , getyval(1))
            botleft = (getxval(2) , getyval(2))
            botright= (getxval(3) , getyval(3))

            masked_image = maskimage(topleft,topright,botright,botleft)

            minpoint = getmin(topleft,topright,botleft,botright)
            maxpoint = getmax(topleft,topright,botleft,botright)

            spot = masked_image[minpoint[1]:maxpoint[1], minpoint[0]:maxpoint[0]]
            histogram(spot,newimg)
            makenewimage(newimg,spot)
    comparehist()