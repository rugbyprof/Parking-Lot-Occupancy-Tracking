import os
from matplotlib import pyplot as plt
import numpy as np
import cv2
import json

histogram_dir = 'Histograms'
spot_dir = 'Spots'

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
    for row in image:
        for col in row:
            sum += col[index]
    print float(sum) / (len(image) * len(image[0]))

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


#cuts a parking spot and resizes the result to 1/10 of the original image
def cutParkingSpot(img, point1, point2, name):
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


with open('newParking.json') as data_file:
    data = json.load(data_file)

img = cv2.imread('oth.jpg')

black_color = (0,0,0)

p_lot = []

#loop through rows in json
for row_data in data:
    #append new row to parking lot
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
        draw_line(img, h_line_obj, black_color)
    
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
                find_max_point(p_lot[-1]['V'][-1], v_line_obj),
                spotName
            )
            saveImg(parking_spot, spot_dir, spotName)

            #make histogram and save
            histogram(parking_spot, spotName)
            
            print spotName, np.average(np.mean(parking_spot, 0), 0)
        #add line object to p_lot
        p_lot[-1]['V'].append(v_line_obj)
        draw_line(img, v_line_obj, black_color)

cv2.imwrite('out.jpg', img)

