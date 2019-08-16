#**************************************************************
#                   Project: Parking-Lot Detection
#                    Names: Kevin Ellis, Anthony Enem
#***************************************************************
#      Place your general program documentation here. It should
#      be quite a few lines explaining the programs duty carefully.
#      It should also indicate how to run the program and data
#     input format, filenames etc
#*****************************************************************
import cv2
import os
import json
from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import urllib2

def getmin(p1,p2,p3,p4):
    #*******************************************************************
    #                    Function Name:: getmin()
    #                   Parameters: Image coordinates
    #       Gets the min Y and X values
    #       Returns (x,y) Pair
    #********************************************************************
    minx =  min(p1[0],p2[0],p3[0],p4[0])
    miny =  min(p1[1],p2[1],p3[1],p4[1])
    return(minx,miny) 
def getmax(p1,p2,p3,p4):
    #*******************************************************************
    #                    Function Name:: getmax()
    #                   Parameters: Image coordinates
    #       Gets the max Y and X values
    #       Returns (x,y) Pair
    #********************************************************************
    maxx =  max(p1[0],p2[0],p3[0],p4[0])
    maxy =  max(p1[1],p2[1],p3[1],p4[1])
    return(maxx,maxy) #Returns (x,y) Pair

def histogram(image,new_image):
    #*******************************************************************
    #                NOT USED CURRENTLY
    #                    Function Name:: histogram()
    #                   Parameters: Image, new image
    #   Calculates the histogram then saves it to the histogram folder
    #********************************************************************
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
def comparehist():
    #*******************************************************************
    #                NOT USED CURRENTLY
    #                    Function Name:: comparehist()
    #                   Parameters: N/A
    #   Uses multiple ways to compare two histograms
    #********************************************************************
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

def saveparkingspace(newimg,spot):
    #*******************************************************************
    #                    Function Name:: saveparkingspace()
    #                   Parameters: imagename,spot image
    #   Calculates the histogram then saves it to the histogram folder
    #********************************************************************
    dirname = 'Spots'
    resizeimage = cv2.resize(spot,(50,70)) #resizes image to 50 x 70
    cv2.imwrite(os.path.join(dirname, newimg + '.jpg'), resizeimage) #saves to Spots Folder

def maskimage(img, topleft,topright,botright,botleft):
    #*******************************************************************
    #                    Function Name:: maskimage()
    #                   Parameters: Image, coordinates
    #   Uses OpenCV fuction to apply a mask to the image. Then
    #   returns the masked image
    #********************************************************************
    mask = np.zeros(img.shape, dtype=np.uint8)
    roi_corners = np.array([[topleft, topright, botright,botleft]], dtype=np.int32)  # fill the ROI so it doesn't get wiped out when the mask is applied
    channel_count = img.shape[2]  # i.e. 3 or 4 depending on your image
    ignore_mask_color = (255,)*channel_count
    cv2.fillPoly(mask, roi_corners, ignore_mask_color)
    masked_image = cv2.bitwise_and(img, mask)  # apply the mask
    return(masked_image)

def average(image,index):
    #*******************************************************************
    #                    Function Name:: average()
    #                   Parameters: Image,index
    #       called by averagecolors function 
    #       calculates the average of one color 
    #********************************************************************
    sum = 0
    count = 0
    for row in image:
        for col in row:
            if col[index] !=0:
                sum += col[index]
                count = count+1
                
    return float(sum) / count

def countwhite(image):
    #*******************************************************************
    #                    Function Name:: countwhite()
    #                   Parameters: image
    #   counts the number of white pixels in the image, also calculates 
    #   the ratio of number of white pixels to entire image
    #********************************************************************
    im=Image.open( "canny edges/"+ parkingspacelocation +"Edge.bmp" )
    width,height = im.size
    actualpixel = width * height #how many pixels in the entire image?
    count = 0
    for row in image:
        for col in row:
            if col == 255:
                count = count + 1
    ratioofwhitepixels = float(actualpixel) / count
    print "Number of pixels in image: " ,actualpixel
    print "Ratio of white to image: " ,ratioofwhitepixels
    return count,ratioofwhitepixels
def averagecolors(image):
    #*******************************************************************
    #                    Function Name:: averagecolors()
    #                   Parameters: image
    #       returns an array of [B,G,R] for that spot
    #********************************************************************
    avg = [average(image,0) , average(image,1) , average(image, 2)]
    return (avg) #returns touple on rgbavg
def cannyedgedetection(spotforcanny):
    #*******************************************************************
    #                    Function Name:: cannyedgedetection()
    #                   Parameters: image
    #   Uses OpenCV fuction to detect edges on the image
    # 
    #********************************************************************
    sigma=0.33
    v = np.median(spotforcanny)

    lower = int(max(0, (1.0 - sigma) * v)) #calulates the lower bound
    upper = int(min(255, (1.0 + sigma) * v)) #calucates the upper bound

    edges = cv2.Canny(spotforcanny,lower,upper) #returns and iamge map

    white = countwhite(edges) #recieves a touple (num whitepixels,ratio of whitepixels to whole image)

    dirname = 'canny edges\\'
    cv2.imwrite(dirname+parkingspacelocation+'Edge.bmp', edges)
    return white


def withinange(avg1, avg2):
    #*******************************************************************
    #                    Function Name:: withinange()
    #                   Parameters: avg1,avg2
    #   gets differences between the color of the current spot and it's empty
    #   counterpart
    #********************************************************************
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


def boxemup(image,topleft,topright,botright,botleft, color):
    #*******************************************************************
    #                    Function Name:: boxemup()
    #                   Parameters: Image, coordiantes, and color
    #   draws the lines to the final image
    #********************************************************************
    line_sz = 2
    diff = 5
    cv2.line(image,(topleft[0] +diff,topleft[1]),(topright[0] -diff,topright[1]),color, line_sz)#1 -> 2
    cv2.line(image,(topleft[0] +diff,topleft[1]),(botleft[0] +diff ,botleft[1]),color, line_sz) #1 -> 3
    cv2.line(image,(topright[0] -diff ,topright[1]),(botright[0] - diff,botright[1]),color, line_sz) #2 -> 4
    cv2.line(image,(botleft[0] +diff,botleft[1]),(botright[0] -diff ,botright[1]),color, line_sz) #3 -> 4
    return image

def drawBoundBox(img, color):
    #*******************************************************************
    #                    Function Name:: drawBoundBox()
    #                   Parameters: Image, color
    #   draws the bounding box of color onto the spot image
    #********************************************************************
    line_size = 5
    #top horizontal line
    cv2.line(img, (0, 0), (len(img[0]), 0), color, line_size) 
    #left vertical line
    cv2.line(img, (0, 0), (0, len(img)), color, line_size)
    #bottom horizontal line
    cv2.line(img, (0, len(img)), (len(img[0]), len(img)), color, line_size)
    #right vertical line
    cv2.line(img, (len(img[0]), 0), (len(img[0]), len(img)), color, line_size)


def saveImgUrl(url, file_name):
    #*******************************************************************
    #                      Function Name:: SaveImgUrl()
    #                    Parameters: The image's URL, and what to call the image
    #   Goes to the Parking-Lot image's URL then saves the image locally
    #   so that we can access and process the image
    #********************************************************************
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

with open('UFPR05_105.json') as data_file: #Pick the JSON that defines the parking lot you are working with
    lot_data = json.load(data_file)

with open('UFPR05_emptyData.json') as emptyLotFile: #Use the JSON that contains information about the parking lot when empty
    emptyLot_data = json.load(emptyLotFile)
red_color = (0,0,255) #Globaly defines the color red
green_color = (0,255,0) #Globaly defines the color green
if __name__ == "__main__":

    lot_shots = lot_data['data']['snapshots'] #Images of Parking-Lot
    lot_coords = lot_data['data']['coords'] #coordinates of spots in the  parking-lot

    numImg = 1 #how many images do you want to run over?

    nonchangenumImg = numImg #saves the number of images being used into a static varible
    addup = 0

    sumoverallaverage = 0 #to calculate average correctness of all images ran

#-------------------(SUBJECT TO CHANGE)--------------------------
    numwhiteratiothreshold = 10 #threshold for numwhiteratio algorithm
    numwhiteratiothresholdstart = numwhiteratiothreshold #where to start the threshold
    numwhiteratiothresholdend = 17 #where to end the threshold
    medianthreshold = 70
    whitediffernecethreshold = 90
#-------------------(SUBJECT TO CHANGE)--------------------------

    for img in lot_shots: #loop through the Parking-Lot images
        if numImg < 1 :
            break #Breaks out of the for-loop if there are no more parking lot images
        
        numImg = numImg - 1 #decrement the number images left

#-----------Calls SaveImgUrl Fuction -------------------
        url = img[1]['img'] #Parking-Lot image's URL
        img_name = img[0]+".jpg" #Gives the Parking-Lot image a name
        saveImgUrl(url, "Origin_Images\\"+img_name) 

        image = cv2.imread('Origin_Images\\' + img_name) #reads the image that was just saved
        
        spotColors = [] #Used to save the color for each spot

#----------FOR CALCULATING PERCENT OF CORRECTNESS---------------
        correctspots = 0 #Used to hold how many spots are taken in the Parking-Lot
        percentcorrect = 0 #Used to hold the value of how correct we we were

        for parkingspot in lot_coords: #loops through the Parking-Lot for each individual spot
            decidedfullorempty = 0 #Used to hold the value (0 or 1) 1 for taken  0 for empty
            
            parkingspacelocation = "Space_#_" + str(parkingspot[0]) #Parking space location in the Parking-Lot

#------------------- GETS THE COORDINATES FOR THE SPOT BEING PROCESSED ------------
            topleft = (int(parkingspot[1][3]['x']),int(parkingspot[1][3]['y'])) 
            topright = (int(parkingspot[1][2]['x']),int(parkingspot[1][2]['y']))        
            botleft = (int(parkingspot[1][0]['x']),int(parkingspot[1][0]['y']))
            botright= (int(parkingspot[1][1]['x']),int(parkingspot[1][1]['y']))

#------------------- CODE THAT APPLYS MASK TO PARKING SPACE -----------------------
            masked_image = maskimage(image,topleft,topright,botright,botleft)
            minpoint = getmin(topleft,topright,botleft,botright)
            maxpoint = getmax(topleft,topright,botleft,botright)
            maskedparkingspace = masked_image[minpoint[1]:maxpoint[1], minpoint[0]:maxpoint[0]]

            denoise = cv2.fastNlMeansDenoisingColored(maskedparkingspace,None,20,21,7,31) #gets rid of image noise
            print(parkingspacelocation)
            #print('Gavg',gray_spot_avg)
            avg = averagecolors(denoise) #gets the average of [R,G,B]
            #print('Cavg',avg)
            colorResult = [withinange(emptyLot_data['spots'][parkingspot[0]-1][1], avg)]


            gray_image = cv2.cvtColor(denoise, cv2.COLOR_BGR2GRAY) #convert the denoise'd image to grayscale
            blur = cv2.GaussianBlur(gray_image,(5,5),0) #blur the image

            numberofwhite = cannyedgedetection(blur) #Calls cannyedgedectection funcion, and recives a touple

            whitediffromempty = numberofwhite[0] - emptyLot_data['spots'][parkingspot[0]-1][2] #Differnce of number of white pixels to the spot and it's empty counterpart

            print "Diff of whitepixels: ", whitediffromempty
            median = np.median(blur) #gets the median of the blurred image
            print "Median: " , median


#-------------BELOW IS WHERE WE APPLY THE ALGORITHMS TO DIFFERENT THRESHOLDS----------------
            if median < medianthreshold: #if yes then the spot is taken
                 drawBoundBox(maskedparkingspace, red_color)
                 spotColors.append([topleft, topright, botleft, botright, red_color])
                 decidedfullorempty = 1
            elif numberofwhite[1] <= numwhiteratiothreshold: #if yes then the spot is taken
                 drawBoundBox(maskedparkingspace, red_color)
                 spotColors.append([topleft, topright, botleft, botright, red_color])
                 decidedfullorempty = 1
            elif whitediffromempty > whitediffernecethreshold: #if yes then the spot is taken
                drawBoundBox(maskedparkingspace, red_color)
                spotColors.append([topleft, topright, botleft, botright, red_color])
                decidedfullorempty = 1
                #color isnt working at the moment
            # elif colorResult[0] == False : #if yes then spot is taken
            #     drawBoundBox(maskedparkingspace, red_color)
            #     spotColors.append([topleft, topright, botleft, botright, red_color]) 
            #     decidedfullorempty = 1    
            else: # else the spot is empty
                drawBoundBox(maskedparkingspace, green_color)
                spotColors.append([topleft, topright, botleft, botright, green_color])
                decidedfullorempty = 0


            if (int(lot_data['data']['snapshots'][addup][1]["lotSnapshot"][str(parkingspot[0])]) == 0):
                print('Actual result from Json: OPEN') #Uses JSON the print the actual status of the spot
            else:  
                print('Actual result from Json: TAKEN') #Uses JSON the print the actual status of the spot

            if (decidedfullorempty == 0):
                print('Our result: OPEN \n') 
            else:  
                print('Our result: TAKEN \n')

            if (int(lot_data['data']['snapshots'][addup][1]["lotSnapshot"][str(parkingspot[0])]) == decidedfullorempty):
                correctspots = correctspots + 1 #if we were correct then incriment the counter

            saveparkingspace(parkingspacelocation,maskedparkingspace) #save the spot

        for spot in spotColors: #loop through the list of spotColors
            image = boxemup(image, spot[0], spot[1], spot[3], spot[2], spot[4]) #applies the color to each spot

        percentcorrect = (float(correctspots) / len(lot_coords)) * 100   
        sumoverallaverage = sumoverallaverage + percentcorrect
        print "Percentage of correct spots for the current image:", percentcorrect
        # ------uses linear interpolation the slowly increment the numwhite threshold --------
        numwhiteratiothreshold =  numwhiteratiothreshold + (numwhiteratiothresholdend - numwhiteratiothresholdstart) / 100.0
        addup = addup + 1
        cv2.imwrite('Output_Images\\'+img_name, image)
    print "\nOverall Percentage of correctness for the experiment:", sumoverallaverage/nonchangenumImg