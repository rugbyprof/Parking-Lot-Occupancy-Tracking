import cv2
import os
import json
from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import urllib2

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

def maskimage(img, topleft,topright,botright,botleft): #Masks the image. 
    mask = np.zeros(img.shape, dtype=np.uint8)
    roi_corners = np.array([[topleft, topright, botright,botleft]], dtype=np.int32)  # fill the ROI so it doesn't get wiped out when the mask is applied
    channel_count = img.shape[2]  # i.e. 3 or 4 depending on your image
    ignore_mask_color = (255,)*channel_count
    cv2.fillPoly(mask, roi_corners, ignore_mask_color)
    masked_image = cv2.bitwise_and(img, mask)  # apply the mask
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

def countwhite(image): #for canny
    im=Image.open( "canny edges/"+ parkingspacelocation +"Edge.bmp" )
    width,height = im.size
    actualpixel = width * height
    count = 0
    for row in image:
        for col in row:
            if col == 255:
                count = count + 1
    ratioofwhitepixels = float(actualpixel) / count
    print "Number of pixels in image: " ,actualpixel
    print "Ratio of white to image: " ,ratioofwhitepixels
    return count,ratioofwhitepixels
def averagecolors(image): #returns an array of [B,G,R] for that spot
    avg = [average(image,0) , average(image,1) , average(image, 2)]
    return (avg) #returns touple on rgbavg
def cannyedgedetection(spotforcanny): #Detects edges
    sigma=0.33
    v = np.median(spotforcanny)

    lower = int(max(0, (1.0 - sigma) * v))
    upper = int(min(255, (1.0 + sigma) * v))

    edges = cv2.Canny(spotforcanny,lower,upper)
    white = countwhite(edges) #recieves a touple (num whitepixels,ratio of white to whole image)

    dirname = 'canny edges\\'
    #plt.savefig(os.path.join(dirname, parkingspacelocation +  'Edge' + '.png'),transparent=True) #Saves the image to Edges folder
    cv2.imwrite(dirname+parkingspacelocation+'Edge.bmp', edges)
    #plt.savefig(os.path.join(dirname, parkingspacelocation +  'Edge' + '.png'),transparent=True) #Saves the image to Edges folder
    #plt.close()
    return white
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

def withinange(avg1, avg2):
    range = 0.1
    blue_diff = abs(avg1[0]-avg2[0])
    green_diff = abs(avg1[1]-avg2[1])
    red_diff = abs(avg1[2]-avg2[2])
    avg_diff = (blue_diff + green_diff + red_diff)/3
    grades = [blue_diff/255.0, green_diff/255.0, red_diff/255.0]
    #print grades
    for grade in grades:
        if grade > range:
            return False
    
    #if grades[0] > range or grades[1] > range or green_diff > range:
    #    return False
    return True
def withinRange(avg1, avg2):
    #range = 0.2
    #print avg1
    #print avg2
    threshold = 4
    blue_diff = abs(avg1[0]-avg2[0])
    green_diff = abs(avg1[1]-avg2[1])
    red_diff = abs(avg1[2]-avg2[2])
    #print(blue_diff, green_diff, red_diff)
    avg_diff = (blue_diff + green_diff + red_diff)/3
    avgbluediff = abs(blue_diff - avg_diff)
    avggreendiff = abs(green_diff - avg_diff)
    avgreddiff = abs(red_diff - avg_diff)
    #print(avgbluediff,avggreendiff,avgreddiff)
    if((abs(blue_diff - avg_diff) < threshold) and (abs(green_diff - avg_diff) < threshold) and (abs(red_diff - avg_diff) < threshold)):
        return True
    else:  
        return False

def compareDiffs(avg1, avg2):
    #AVG as [B, G, R]
    max_diff = 3.0
    fails = 0
    BG1_diff = abs(avg1[0] - avg1[1])
    BR1_diff = abs(avg1[0] - avg1[2])
    GR1_diff = abs(avg1[1] - avg1[2])

    BG2_diff = abs(avg2[0] - avg2[1])
    BR2_diff = abs(avg2[0] - avg2[2])
    GR2_diff = abs(avg2[1] - avg2[2])

    BG_diff = abs(BG1_diff - BG2_diff)
    BR_diff = abs(BR1_diff - BR2_diff)
    GR_diff = abs(GR1_diff - GR2_diff)

    #print avg2
    #print avg1
    #print avg2
    #print BG1_diff, BR1_diff, GR1_diff
    #print BG2_diff, BR2_diff, GR2_diff
    #print BG_diff, BR_diff, GR_diff
    #print spotName, ":", "BG: ", BG_diff/255.0, "BR: ", BR_diff/255.0, "GR: ", GR_diff/255.0, "\n"
    if BG_diff > max_diff:
        fails = fails + 1
    if BR_diff > max_diff:
        fails = fails + 1
    if GR_diff > max_diff:
        fails = fails + 1
    if(fails > 1):
        return False
    return True

def boxemup(image,topleft,topright,botright,botleft, color):
    line_sz = 2
    diff = 5
    cv2.line(image,(topleft[0] +diff,topleft[1]),(topright[0] -diff,topright[1]),color, line_sz)#1 -> 2
    cv2.line(image,(topleft[0] +diff,topleft[1]),(botleft[0] +diff ,botleft[1]),color, line_sz) #1 -> 3
    cv2.line(image,(topright[0] -diff ,topright[1]),(botright[0] - diff,botright[1]),color, line_sz) #2 -> 4
    cv2.line(image,(botleft[0] +diff,botleft[1]),(botright[0] -diff ,botright[1]),color, line_sz) #3 -> 4
    return image

def drawBoundBox(img, color):
    line_size = 5
    #top horizontal line
    cv2.line(img, (0, 0), (len(img[0]), 0), color, line_size) 
    #left vertical line
    cv2.line(img, (0, 0), (0, len(img)), color, line_size)
    #bottom horizontal line
    cv2.line(img, (0, len(img)), (len(img[0]), len(img)), color, line_size)
    #right vertical line
    cv2.line(img, (len(img[0]), 0), (len(img[0]), len(img)), color, line_size)

#save image from url

def saveImgUrl(url, file_name):
    #url = "http://download.thinkbroadband.com/10MB.zip"
    #file_name = 'Origin_Images\\' + (url.split('/')[-1])
    u = urllib2.urlopen(url)
    infile = open(file_name, 'wb')
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
        infile.write(buffer)
        status = r"%10d  [%3.2f%%]" % (file_size_dl, file_size_dl * 100. / file_size)
        status = status + chr(8)*(len(status)+1)
        print status,
    infile.close()


with open('out.json') as data_file:
    lot_data = json.load(data_file)

with open('UFPR05_emptyData.json') as emptyLotFile:
    emptyLot_data = json.load(emptyLotFile)

if __name__ == "__main__":

    numImg = 100 #how many images to run over?
    nonchangenumImg = numImg
    addup = 0
    lot_shots = lot_data['data']['snapshots'] #snapshots of actual p-lots
    lot_coords = lot_data['data']['coords'] #coordinates of spots in p-lot

    #loop through snapshots
    sumoverallaverage = 0 #to calculate average correctness of all images ran
    numwhiteratiothreshold = 10 #threshold for numwhiteratio algorithm
    numwhiteratiothresholdstart = numwhiteratiothreshold #where to start threshold
    numwhiteratiothresholdend = 17 #where to end threshold
    for img in lot_shots: #loop through the images
        if numImg < 1 :
            break
        
        numImg = numImg - 1
        addup = addup + 1
        url = img[1]['img'] #snapshot's url
        
        img_name = img[0]+".jpg"

        saveImgUrl(url, "Origin_Images\\"+img_name) #save img from url
        image = cv2.imread('Origin_Images\\' + img_name)

        #image = cv2.resize(image,(640,480))
        red_color = (0,0,255)
        green_color = (0,255,0)
        blue_color= (255,0,0)
        
        spotColors = []
        sumoftakenspots = 0
        percentcorrect = 0
        for parkingspot in lot_coords:
            decidedfullorempty = 0
            parkingspacelocation = "Space_#_" + str(parkingspot[0]) #item 0 is the spot number
            topleft = (int(parkingspot[1][3]['x']),int(parkingspot[1][3]['y']))
            topright = (int(parkingspot[1][2]['x']),int(parkingspot[1][2]['y']))
            botleft = (int(parkingspot[1][0]['x']),int(parkingspot[1][0]['y']))
            botright= (int(parkingspot[1][1]['x']),int(parkingspot[1][1]['y']))
            #print (topleft, topright, botleft, botright)

            #  CODE THAT APPLYS MASK TO PARKING SPACE
            masked_image = maskimage(image,topleft,topright,botright,botleft)
            minpoint = getmin(topleft,topright,botleft,botright)
            maxpoint = getmax(topleft,topright,botleft,botright)
            maskedparkingspace = masked_image[minpoint[1]:maxpoint[1], minpoint[0]:maxpoint[0]]
            #histogram(maskedparkingspace,parkingspacelocation)

            #  FOR COLOR DETECTION 
            denoise = cv2.fastNlMeansDenoisingColored(maskedparkingspace,None,20,21,7,31)
            print(parkingspacelocation)
            #print('Gavg',gray_spot_avg)
            avg = averagecolors(denoise)
            #print('Cavg',avg)
            colorResult = [withinange(emptyLot_data['spots'][parkingspot[0]-1][1], avg), 
            compareDiffs(emptyLot_data['spots'][parkingspot[0]-1][1], avg)]

            #FOR EDGE DETECTION
            gray_image = cv2.cvtColor(denoise, cv2.COLOR_BGR2GRAY)
            blur = cv2.GaussianBlur(gray_image,(5,5),0)
            numberofwhite = cannyedgedetection(blur) #recives a touple
            whitediffromempty = numberofwhite[0] - emptyLot_data['spots'][parkingspot[0]-1][2]
            #print numberofwhite[0], emptyLot_data['spots'][parkingspot[0]-1][2]
            print "Diff of whitepixels: ", whitediffromempty
            median = np.median(blur)
            print "Median: " , median


            #--BELOW IS WHERE WE APPLY THE ALGORITHMS TO DIFFERENT THRESHOLDS--
            if median < 70: #if yes then the spot is taken
                 drawBoundBox(maskedparkingspace, red_color)
                 spotColors.append([topleft, topright, botleft, botright, red_color])
                 decidedfullorempty = 1
            elif numberofwhite[1] <= numwhiteratiothreshold: #if yes then the spot is taken   #was 17
                 drawBoundBox(maskedparkingspace, red_color)
                 spotColors.append([topleft, topright, botleft, botright, red_color])
                 decidedfullorempty = 1
            elif whitediffromempty > 90: #if yes then the spot is taken
                drawBoundBox(maskedparkingspace, red_color)
                spotColors.append([topleft, topright, botleft, botright, red_color])
                decidedfullorempty = 1
            # elif colorResult[0] == False or colorResult[1] == False: #if yes then spot is taken
            #     drawBoundBox(maskedparkingspace, red_color)
            #     spotColors.append([topleft, topright, botleft, botright, red_color]) 
            #     decidedfullorempty = 1    
            else: # else the spot is empty
                drawBoundBox(maskedparkingspace, green_color)
                spotColors.append([topleft, topright, botleft, botright, green_color])
                decidedfullorempty = 0


            if (int(lot_data['data']['snapshots'][addup][1]["lotSnapshot"][str(parkingspot[0])]) == 0):
                print('OPEN \n')
            else:  
                print('TAKEN \n')
            
            if (int(lot_data['data']['snapshots'][addup][1]["lotSnapshot"][str(parkingspot[0])]) == decidedfullorempty):
                sumoftakenspots = sumoftakenspots + 1
            saveparkingspace(parkingspacelocation,maskedparkingspace)

        for spot in spotColors:
            image = boxemup(image, spot[0], spot[1], spot[3], spot[2], spot[4])
        print(sumoftakenspots)
        percentcorrect = (float(sumoftakenspots) / 40) * 100
        sumoverallaverage = sumoverallaverage + percentcorrect
        print(percentcorrect)
        print(numwhiteratiothreshold)
        numwhiteratiothreshold =  numwhiteratiothreshold + (numwhiteratiothresholdend - numwhiteratiothresholdstart) / 100.0
        cv2.imwrite('Output_Images\\'+img_name, image)
    print(sumoverallaverage)