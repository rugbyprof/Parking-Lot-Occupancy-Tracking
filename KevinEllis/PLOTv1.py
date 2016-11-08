import cv2
import os
import json
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mpimg

def getmin(p1,p2,p3,p4): #Gets the min Y and X values
    minx =  min(p1[0],p2[0],p3[0],p4[0])
    miny =  min(p1[1],p2[1],p3[1],p4[1])
    return(minx,miny) #Returns (x,y) Pair
def getmax(p1,p2,p3,p4): #Gets the max Y and X values
    maxx =  max(p1[0],p2[0],p3[0],p4[0])
    maxy =  max(p1[1],p2[1],p3[1],p4[1])
    return(maxx,maxy) #Returns (x,y) Pair
def histogram(image,new_image): #Creates a Histogram
    chans = cv2.split(image) # grab the image channels, initialize the tuple of colors,
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
    plt.savefig(os.path.join(dirname, new_image +  'Hist' + '.png')) #Saves the image to Histogram folder
    plt.close()
def comparehist(): #not used ATM
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

def getxval(num): #Gets the X value of spot from JSON
    xval = int(data['Row'+str(row)+'_Col'+str(col)][num]['x'])
    return (xval) 
def getyval(num): #Gets the X value of spot from JSON
    yval = int(data['Row'+str(row)+'_Col'+str(col)][num]['y'])
    return (yval)
def drawline(topleft,topright,botright,botleft,img): #Draws the Lines to the image
    cv2.line(img,(topleft[0],topleft[1]),(topright[0],topright[1]),(255,0,0),1)#1 -> 2
    cv2.line(img,(topleft[0],topleft[1]),(botleft[0],botleft[1]),(255,0,0),1) #1 -> 3
    cv2.line(img,(topright[0],topright[1]),(botright[0],botright[1]),(255,0,0),1) #2 -> 4
    cv2.line(img,(botleft[0],botleft[1]),(botright[0],botright[1]),(255,0,0),1) #3 -> 4
    cv2.imwrite("Lines.jpg",img) #Creates an image Called Lines.jpg

def saveparkingspace(newimg,spot): #Saves each Individual spot in Spots Folder
    dirname = 'Spots'
    resizeimage = cv2.resize(spot,(50,70)) #resizes image to 50 x 70
    cv2.imwrite(os.path.join(dirname, newimg + '.jpg'), resizeimage)
def maskimage(topleft,topright,botright,botleft): #Masks the image. 
    mask = np.zeros(image.shape, dtype=np.uint8)
    roi_corners = np.array([[topleft, topright, botright,botleft]], dtype=np.int32)  # fill the ROI so it doesn't get wiped out when the mask is applied
    channel_count = image.shape[2]  # i.e. 3 or 4 depending on your image
    ignore_mask_color = (255,)*channel_count
    cv2.fillPoly(mask, roi_corners, ignore_mask_color)
    masked_image = cv2.bitwise_and(image, mask)  # apply the mask
    return(masked_image)
def average(image,index): #called by averagecolors function
    sum = 0
    count = 0
    for row in image:
        for col in row:
            if col[index] !=0:
                sum += col[index]
                count = count+1
    return float(sum) / count

def averagecolors(image): #returns an array of [R,G,B] for that spot
    avg = [average(image,0) , average(image,1) , average(image, 2)]
    return (avg) #returns touple on rgbavg
def detectviacolor(spotbeinglookedat): #VERY IMPORTANT NEEDS TWEAKING DOES NOT WORK
    redchange = abs(spotbeinglookedat[0] - 160.4572)
    greenchange = abs(spotbeinglookedat[1] - 151.398)
    bluechange = abs(spotbeinglookedat[2] - 141.49)
    #print(redchange,greenchange,bluechange)
    if (redchange > 6 or greenchange > 20 or bluechange > 45):
        #print("Spot Full! ")
        return
    else:
        #print("Spot Empty! ")
        return
def cannyedgedetection(spotforcanny,parkingspacelocation): #Detects edges
    sigma=0.30
    v = np.median(spotforcanny)
    lower = int(max(0, (1.0 - sigma) * v))
    upper = int(min(255, (1.0 + sigma) * v))
    edges = cv2.Canny(spotforcanny,lower,upper)
    #plt.subplot(121),plt.imshow(spotforcanny,cmap = 'gray')
    #plt.title('Original Image'), plt.xticks([]), plt.yticks([])
    plt.plot(122),plt.imshow(edges,cmap = 'gray')
    plt.title('Edge Image'), plt.xticks([]), plt.yticks([])
    dirname = 'edges'
    plt.savefig(os.path.join(dirname, parkingspacelocation +  'Edge' + '.png'),transparent=True) #Saves the image to Edges folder
    plt.close()
def sharpen(spot): #Sharpens the image for better edge detection
    #Create the identity filter, but with the 1 shifted to the right!
    kernel = np.zeros( (9,9), np.float32)
    kernel[4,4] = 2.0   #Identity, times two! 
    #Create a box filter:
    boxFilter = np.ones( (9,9), np.float32) / 81.0
    #Subtract the two:
    kernel = kernel - boxFilter
    #Note that we are subject to overflow and underflow here...but I believe that
    # filter2D clips top and bottom ranges on the output, plus you'd need a
    # very bright or very dark pixel surrounded by the opposite type.
    custom = cv2.filter2D(spot, -1, kernel)
    return custom
def detectviacanny(): #### WORK IN PROGRESS
    cv2.imread('Row_1 Col0Edge.png', -1)

    return
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
            parkingspacelocation = 'Row_' + str(row) + ' Col_' + str(col)
            topleft = (getxval(0) , getyval(0))
            topright = (getxval(1) , getyval(1))
            botleft = (getxval(2) , getyval(2))
            botright= (getxval(3) , getyval(3))

            masked_image = maskimage(topleft,topright,botright,botleft)
            minpoint = getmin(topleft,topright,botleft,botright)
            maxpoint = getmax(topleft,topright,botleft,botright)
            maskedparkingspace = masked_image[minpoint[1]:maxpoint[1], minpoint[0]:maxpoint[0]]

            histogram(maskedparkingspace,parkingspacelocation)
            saveparkingspace(parkingspacelocation,maskedparkingspace)
            #spotrgb = averagecolors(spot)
            gray_image = cv2.cvtColor(maskedparkingspace, cv2.COLOR_BGR2GRAY)
            sharp = sharpen(gray_image)
            cannyedgedetection(sharp,parkingspacelocation)