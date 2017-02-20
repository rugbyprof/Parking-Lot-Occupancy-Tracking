import os
from matplotlib import pyplot as plt
import numpy as np
import cv2
import json
import sys
import urllib2
from pylab import *

histogram_dir = 'Histograms'
spot_dir = 'Spots'
spots = {}

#class definition for a Point
class Point:
    #constructor
    def __init__(self, point_array):
        self.x = point_array[0]
        self.y = point_array[1]


#class definition for a Line
class Line:
    #constructor
    def __init__(self, point_array1, point_array2):
        self.startPt = Point(point_array1)
        self.endPt = Point(point_array2)
        self.compute_slope()
        self.compute_y_int()
    
    #method for calculating slope
    def compute_slope(self):
        self.slope = float(self.endPt.y - self.startPt.y) / float(self.endPt.x - self.startPt.x)

    #method for calculating y intercept
    def compute_y_int(self):
        self.yInt = float(self.startPt.y - self.slope*self.startPt.x)
        
    #method for getting intersection point with another line
    def get_line_intersect(self, line):
        x = float(self.yInt - line.yInt) / float(line.slope - self.slope)
        y = self.slope*x + self.yInt
        pt = Point(x, y)
        return pt

    #method for getting y intersection for some x coordinate
    def get_y_intersect(self, x):
        y = int(round(self.slope*x + self.yInt))
        return y


def average(image, index):
    sum = 0
    count = 0
    for row in image:
        for col in row:
            if col[index] != 0:
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

def averageColors(image):
    avg = [average(image, 0), average(image, 1), average(image, 2)]
    return avg

#same image to file
def saveImg(img, dir, name):
    cv2.imwrite(os.path.join(dir, name + ".jpg"), img)

#create histogram and save figure
def histogram(image, name):
    # grab the image channels, initialize the tuple of colors,
    # the figure and the flattened feature vector
    chans = cv2.split(image)
    #print chans

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
        #hist_3d = cv2.calcHist([image], [0, 1, 2], None, [8, 8, 8], [0, 256, 0, 256, 0, 256])
    	#hist_3d = cv2.normalize(hist_3d).flatten()
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
    #print "flattened feature vector size: %d" % (np.array(features).flatten().shape)
    

    #save figure and close
    plt.savefig(os.path.join(histogram_dir, "Hist_" + name + ".png"))
    plt.close()

#compare histograms
def compareHistograms():
    # METHOD #1: UTILIZING OPENCV
    # initialize OpenCV methods for histogram comparison
    OPENCV_METHODS = (
            ("Correlation", cv2.HISTCMP_CORREL),
            ("Chi-Squared", cv2.HISTCMP_CHISQR),
            ("Intersection", cv2.HISTCMP_INTERSECT), 
            ("Hellinger", cv2.HISTCMP_BHATTACHARYYA)
        )
        
    # loop over the comparison methods
    for (methodName, method) in OPENCV_METHODS:
        # initialize the results dictionary and the sort
        # direction
        results = {}
        reverse = False

        # if we are using the correlation or intersection
        # method, then sort the results in reverse order
        if methodName in ("Correlation", "Intersection"):
            reverse = True
        for (k, image) in spots.items():
            # compute the distance between the two histograms
            # using the method and update the results dictionary
            hist = cv2.calcHist([image], [0, 1, 2], None, [8, 8, 8], [0, 256, 0, 256, 0, 256])
            hist_norm = hist
            cv2.normalize(hist, hist_norm)
            hist_norm.flatten()

            h1 = cv2.calcHist([spots["1_Gray_Spot"]], [0, 1, 2], None, [8, 8, 8], [0, 256, 0, 256, 0, 256])
            h1_norm = h1
            cv2.normalize(h1, h1_norm)
            h1_norm.flatten()

            d = cv2.compareHist(h1_norm, hist_norm, method)
            results[k] = d
    
        # sort the results
        results = sorted([(v, k) for (k, v) in results.items()], reverse = reverse)
        # show the query image
        fig = plt.figure("Query")
        ax = fig.add_subplot(1, 1, 1)
        ax.imshow(spots["1_Gray_Spot"])
        plt.axis("off")
    
        # initialize the results figure
        fig = plt.figure("Results: %s" % (methodName))
        fig.suptitle(methodName, fontsize = 20)
    
        # loop over the results
        for (i, (v, k)) in enumerate(results):
            # show the result
            ax = fig.add_subplot(1, len(spots), i + 1)
            ax.set_title("%s: %.2f" % (k, v))
            plt.imshow(spots[k])
            plt.axis("off")
    
    # show the OpenCV methods
    plt.show()



#cuts a parking spot and resizes the result to 1/10 of the original image
def cutParkingSpot(img, point1, point2):
    parkingSpot = img[point1.y:point2.y, point1.x:point2.x]
    width, height = img.shape[:2]
    w,h = parkingSpot.shape[:2]
    resized_img = cv2.resize(parkingSpot, (width/10, height/10))

    return resized_img
    

#draws line with color between point1 and point2 on img
def draw_line(img, line, color):
    cv2.line(img, (line.startPt.x, line.startPt.y), (line.endPt.x, line.endPt.y), color, 1)


#finds minimum x and y values from end points of 2 lines
def find_min_point(line1, line2):
    min_x = min(line1.startPt.x, line1.endPt.x, line2.startPt.x, line2.endPt.x)
    min_y = min(line1.startPt.y, line1.endPt.y, line2.startPt.y, line2.endPt.y)

    min_point = Point([min_x, min_y])
    return min_point


#finds maximum x and y values from end points of 2 lines
def find_max_point(line1, line2):
    max_x = max(line1.startPt.x, line1.endPt.x, line2.startPt.x, line2.endPt.x)
    max_y = max(line1.startPt.y, line1.endPt.y, line2.startPt.y, line2.endPt.y)

    max_point = Point([max_x, max_y])
    return max_point


#returns a masked image given the original image, and two horizontal lines defining
#the region of interest
def maskImage(img, ver_line1, ver_line2):
    top_left = (ver_line1.startPt.x, ver_line1.startPt.y)
    bot_left = (ver_line1.endPt.x, ver_line1.endPt.y)
    top_right = (ver_line2.startPt.x, ver_line2.startPt.y)
    bot_right = (ver_line2.endPt.x, ver_line2.endPt.y)

    mask = np.zeros(img.shape, dtype=np.uint8)
    roi_corners = np.array([[top_left, top_right, bot_right,bot_left]], dtype=np.int32)  # fill the ROI so it doesn't get wiped out when the mask is applied
    channel_count = img.shape[2]  # i.e. 3 or 4 depending on your image
    ignore_mask_color = (255,)*channel_count
    cv2.fillPoly(mask, roi_corners, ignore_mask_color)
    masked_image = cv2.bitwise_and(img, mask)  # apply the mask
    return(masked_image)

#compares img1 to img2 based on their average values
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

def compareDiffs(avg1, avg2, spotName):
    #AVG as [B, G, R]
    max_diff = 2.0
    fails = 0
    BG1_diff = avg1[0] - avg1[1]
    BR1_diff = avg1[0] - avg1[2]
    GR1_diff = avg1[1] - avg1[2]

    BG2_diff = avg2[0] - avg2[1]
    BR2_diff = avg2[0] - avg2[2]
    GR2_diff = avg2[1] - avg2[2]

    BG_diff = abs(BG1_diff - BG2_diff)
    BR_diff = abs(BR1_diff - BR2_diff)
    GR_diff = abs(GR1_diff - GR2_diff)

    #print avg2
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

#save image from url
def saveImgUrl(url):
    #url = "http://download.thinkbroadband.com/10MB.zip"
    file_name = 'Origin_Images\\' + (url.split('/')[-1])
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

#draw bounding box using lines of specified color around the image
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

def cannyedgedetection(spotforcanny,parkingspacelocation): #Detects edges
    sigma=0.30
    v = np.median(spotforcanny)
    lower = int(max(0, (1.0 - sigma) * v))
    upper = int(min(255, (1.0 + sigma) * v))
    edges = cv2.Canny(spotforcanny,lower,upper)
    #print edges
    avg = averagePng(edges)
    #print parkingspacelocation, avg
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

def boxemup(image, left, right, color):
    line_sz = 2
    diff = 4

    #top hor
    cv2.line(image, (left.startPt.x+diff, left.startPt.y), (right.startPt.x-diff, right.startPt.y), color, line_sz)
    #bot hor
    cv2.line(image, (left.endPt.x+diff, left.endPt.y), (right.endPt.x-diff, right.endPt.y), color, line_sz)
    #left vert
    cv2.line(image, (left.startPt.x+diff, left.startPt.y), (left.endPt.x+diff, left.endPt.y), color, line_sz)
    #right vert
    cv2.line(image, (right.startPt.x-diff, right.startPt.y), (right.endPt.x-diff, right.endPt.y), color, line_sz)

    return image

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




with open('newJson.json') as data_file:
    data = json.load(data_file)

black_color = (0,0,0)
red_color = (0,0,255)
green_color = (0,255,0)

#all images taken at timeOfDay
timeOfDay = '1100'
req = urllib2.urlopen('http://cs.mwsu.edu/~griffin/p-lot/apiproxy.php?time=' + timeOfDay)
req = ''.join(req)

f = open("images.json", "w")

p_json = json.loads(req)
f.write(p_json)
f.close()
numImgs = 0

with open('images.json') as images_file:
    images = json.load(images_file)

#loop through all images
for image in images['data']:

    if numImgs > 10:
        break
    numImgs = numImgs + 1

    #get image url and save image as a local file
    url = image['shot_url']+image['camera']+'/'+image['name']
    resultName = image['name']
    saveImgUrl(url)

    img = cv2.imread('Origin_Images\\' + image['name'])

    p_lot = []
    gray_spot = []
    gray_spot_avg = []
    spot_result = ""

    gray = data["0"]
    #loop through rows in json
    for row_data in data:
        #append new row to parking lot
        size = sys.getsizeof(row_data[0])

        if size == 12: #check for gray spot
            w,h = img.shape[:2]
            pt = Point(row_data)
            pt1 = Point([pt.x+h/10, pt.y+w/10])
            #print size, h/10, w/10
            gray_spot = cutParkingSpot(img, pt, pt1)
            gray_spot_avg = averageColors(gray_spot)
            #print "Gray Spot", gray_spot_avg
            #cv2.imshow("Grayspot", gray_spot)
            #cv2.waitKey(0)
            saveImg(gray_spot, spot_dir, "1_Gray_Spot")
            spots["1_Gray_Spot"] = gray_spot
            histogram(gray_spot, "1_Gray_Spot")
            continue #break out

        p_lot.append(
            {
                'H': [], #list of horizontals
                'V': [] #list of verticals
            }
        )

        #process horizontal lines  
        for h_line in row_data[0]:
            h_line_obj = Line(h_line[0], h_line[1]) #get new Line object
            p_lot[-1]['H'].append(h_line_obj) #add new object to p_lot
            #draw_line(img, h_line_obj, black_color)
        
        top_h_line = p_lot[-1]['H'][0]
        bot_h_line = p_lot[-1]['H'][1]

        #process vertical lines
        for v_line in row_data[1]:
            #create Line object for vertical line
            v_line_obj = Line(
                    [v_line[0], top_h_line.get_y_intersect(v_line[0])], 
                    [v_line[1], bot_h_line.get_y_intersect(v_line[1])]
                )
            
            #Start extracting spots after first vertical line
            if len(p_lot[-1]['V']) > 0:            
                #mask image
                maskedImg = maskImage(img, p_lot[-1]['V'][-1], v_line_obj)

                #get row and column of spot
                spotName = "Row_" + str(len(p_lot)) + "_Col_" + str(len(p_lot[-1]['V']))

                #extract spot from maskedImage and save
                parking_spot = cutParkingSpot(
                    maskedImg, 
                    find_min_point(p_lot[-1]['V'][-1], v_line_obj), 
                    find_max_point(p_lot[-1]['V'][-1], v_line_obj)
                )

                #make histogram and save
                #histogram(parking_spot, spotName)
                
                #averaging values of red, green and blue colors in parking spot image
                #print spotName, np.average(np.mean(parking_spot, 0), 0)
                avg = averageColors(parking_spot)
                #print spotName, avg
                spots[spotName] = parking_spot
                colorResult = withinRange(gray_spot_avg, avg, spotName) 

                gray_image = cv2.cvtColor(parking_spot, cv2.COLOR_BGR2GRAY)
                sharp = sharpen(gray_image)
                edgesResult = cannyedgedetection(sharp,spotName)

                #give spot specific color based on results

                #false positives HARD CODED
                #if spotName == "Row_2_Col_1" or spotName == "Row_2_Col_12":
                    #img = boxemup(img, p_lot[-1]['V'][-1], v_line_obj, (255,0,0))   

                if colorResult == False: #negatives (filled spots) from color test
                    drawBoundBox(parking_spot, red_color)
                    img = boxemup(img, p_lot[-1]['V'][-1], v_line_obj, red_color)   


                elif edgesResult[0] == False: #negatives (filled spots) from edge detection test
                    drawBoundBox(parking_spot, red_color)
                    img = boxemup(img, p_lot[-1]['V'][-1], v_line_obj, red_color)      

                else: #others are assumed to be positives (empty spots)
                    drawBoundBox(parking_spot, green_color)
                    img = boxemup(img, p_lot[-1]['V'][-1], v_line_obj, green_color)     
                   
                #cv2.imshow("edges", edgesResult[1])

                saveImg(parking_spot, spot_dir, spotName)
                
            #add line object to p_lot
            p_lot[-1]['V'].append(v_line_obj)
            #draw_line(img, v_line_obj, black_color)

    #compareHistograms()
    cv2.imwrite(os.path.join('results', resultName + '.jpg'), img)

