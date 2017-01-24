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

    #IS THIS NEEDED ANYMORE?
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

def averagePng(image):
    count = 0
    for row in image:
        for col in row:
            if col == 255:
                count = count + 1
    
    return count
def averagecolors(image): #returns an array of [R,G,B] for that spot
    avg = [average(image,0) , average(image,1) , average(image, 2)]
    return (avg) #returns touple on rgbavg
def cannyedgedetection(spotforcanny,parkingspacelocation): #Detects edges
    sigma=0.30
    v = np.median(spotforcanny)
    lower = int(max(0, (1.0 - sigma) * v))
    upper = int(min(255, (1.0 + sigma) * v))
    edges = cv2.Canny(spotforcanny,lower,upper)
    avg = averagePng(edges)
    #plt.subplot(121),plt.imshow(spotforcanny,cmap = 'gray')
    #plt.title('Original Image'), plt.xticks([]), plt.yticks([])
    plt.plot(122),plt.imshow(edges,cmap = 'gray')
    plt.title('Edge Image'), plt.xticks([]), plt.yticks([])
    dirname = 'canny edges'
    plt.savefig(os.path.join(dirname, parkingspacelocation +  'Edge' + '.png'),transparent=True) #Saves the image to Edges folder
    plt.close()
    
    if avg > 400:
        return False,edges
    return True,edges

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

def withinRange(avg1, avg2, spotName):
    range = 0.2
    blue_diff = abs(avg1[0]-avg2[0])
    green_diff = abs(avg1[1]-avg2[1])
    red_diff = abs(avg1[2]-avg2[2])
    avg_diff = (blue_diff + green_diff + red_diff)/3
    grades = [blue_diff/255.0, green_diff/255.0, red_diff/255.0]
    #print spotName, grades
    
    for grade in grades:
        if grade > range:
            return False
    
    #if grades[0] > range or grades[1] > range or green_diff > range:
    #    return False
    return True

    #if blue_diff > range or green_diff > range or red_diff > range:
    #    return False
    #return True

def boxemup(image,topleft,topright,botright,botleft, color):
    line_sz = 2
    diff = 5
    cv2.line(image,(topleft[0] +diff,topleft[1]),(topright[0] -diff,topright[1]),color, line_sz)#1 -> 2
    cv2.line(image,(topleft[0] +diff,topleft[1]),(botleft[0] +diff ,botleft[1]),color, line_sz) #1 -> 3
    cv2.line(image,(topright[0] -diff ,topright[1]),(botright[0] - diff,botright[1]),color, line_sz) #2 -> 4
    cv2.line(image,(botleft[0] +diff,botleft[1]),(botright[0] -diff ,botright[1]),color, line_sz) #3 -> 4
    return image

def drawBoundBox(img,  color):
    line_size = 3
    #top horizontal line
    cv2.line(img, (0, 0), (0, len(img[0])), color, line_size) 
    #left vertical line
    cv2.line(img, (0, 0), (0, len(img)), color, line_size)
    #bottom horizontal line
    cv2.line(img, (0, len(img)), (len(img[0]), len(img)), color, line_size)
    #right vertical line
    cv2.line(img, (len(img[0]), 0), (len(img[0]), len(img)), color, line_size)

if __name__ == "__main__":
    image = cv2.imread('image2.jpg', -1)
    image = cv2.resize(image,(640,480))
    red_color = (0,0,255)
    green_color = (0,255,0) 
    with open('parking.json') as data_file:
        data = json.load(data_file)
    for row in range (0,3):#0 -> number of rows of spots [fix with griffin's json]
        if row == 0:
            numspots = 5
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

            #  CODE THAT APPLYS MASK TO PARKING SPACE
            masked_image = maskimage(topleft,topright,botright,botleft)
            minpoint = getmin(topleft,topright,botleft,botright)
            maxpoint = getmax(topleft,topright,botleft,botright)
            maskedparkingspace = masked_image[minpoint[1]:maxpoint[1], minpoint[0]:maxpoint[0]]
            #histogram(maskedparkingspace,parkingspacelocation)

            saveparkingspace(parkingspacelocation,maskedparkingspace)


            #  FOR COLOR DETECTION 
            gray_spot = cv2.imread('Spots/Row_0 Col_0.jpg')
            gray_spot_avg = averagecolors(gray_spot)
            avg = averagecolors(maskedparkingspace)
            colorResult = withinRange(gray_spot_avg, avg, parkingspacelocation) 

            #FOR EDGE DETECTION
            gray_image = cv2.cvtColor(maskedparkingspace, cv2.COLOR_BGR2GRAY)
            sharp = sharpen(gray_image)
            edgesResult = cannyedgedetection(sharp,parkingspacelocation)


            if colorResult == False:
                drawBoundBox(maskedparkingspace, red_color)
                image = boxemup(image ,topleft,topright,botright,botleft, red_color)                        
            elif edgesResult[0] == False:
                drawBoundBox(maskedparkingspace, red_color)
                image  = boxemup(image ,topleft,topright,botright,botleft, red_color)       
            else:
                drawBoundBox(maskedparkingspace, green_color)
                image  = boxemup(image ,topleft,topright,botright,botleft, green_color)     
cv2.imwrite('out.jpg', image)