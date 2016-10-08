from matplotlib import pyplot as plt
import numpy as np
import cv2
import json

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

def cutParkingSpot(img, point1, point2, idx):
    print "clipping: ", point1.x, point1.y, point2.x, point2.y
    parkingSpot = img[point1.y:point2.y, point1.x:point2.x]
    width, height = img.shape[:2]
    print width, height
    w,h = parkingSpot.shape[:2]
    print "w:h:", w,h
    res = cv2.resize(parkingSpot, (width/3, height/3))
    cv2.imshow("spot created", res)
    histogram(res)
    
    #cv2.imwrite('spot'+str(idx)+'.jpg',res)
    #cv2.imshow("m", img)
    cv2.waitKey(0)
    return
    
#draws line with color between point1 and point2 on img
def draw_line(img, line, color):
    cv2.line(img, (line.startPt.x, line.startPt.y), (line.endPt.x, line.endPt.y), color, 1)



with open('lot.json') as data_file:
    data = json.load(data_file)

img = cv2.imread('img.jpg')

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
        
        #if len(p_lot[-1]['V']) > 0:
            #cutParkingSpot(img, p_lot[-1]['V'][-1].startPt, v_line_obj.endPt, len(p_lot[-1]['V']))

        #add object to p_lot
        p_lot[-1]['V'].append(v_line_obj)
        draw_line(img, v_line_obj, black_color)

        

cv2.imwrite('out.jpg', img)

