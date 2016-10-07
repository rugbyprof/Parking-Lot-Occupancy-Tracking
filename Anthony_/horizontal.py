from matplotlib import pyplot as plt
import numpy as np
import cv2
import json

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

def cutParkingSpot(img, points, idx):
    print "clipping: ", points[0]['x'], points[0]['y'], points[1]['x'], points[1]['y']
    parkingSpot = img[480 - int(points[0]['y']):480-int(points[1]['y']), int(points[0]['x']):int(points[1]['x'])]
    new_p_spot = img[480-int(points[0]['y']):480-int(points[1]['y']), int(points[0]['x']):int(points[1]['x'])]
    width, height = img.shape[:2]
    print width, height
    w,h = parkingSpot.shape[:2]
    print "w:h:", w,h
    res = cv2.resize(parkingSpot, (width/3, height/3))
    histogram(res)
    cv2.imshow("spot created", res)
    #cv2.imwrite('spot'+str(idx)+'.jpg',res)
    #cv2.imshow("m", img)
    cv2.waitKey(0)
    return

#find intersect between line and x coordinate
def find_Y_Intersect(line, x):
    intersect = int(round(line["slope"]*x + line["yInt"]))
    return intersect

#find intersect of 2 lines
def lines_intersect(line1, line2):
    print "intersect:", line1["slope"], line1["yInt"], line2["slope"], line2["yInt"]
    x = float(abs(line2["yInt"] - line1["yInt"])) / float(abs(line1["slope"] - line2["slope"]))
    y = line1["slope"]*x + line1["yInt"]
    print "returned:", x, y
    return [x, y]

#find slope of line
def find_Slope(line):
    slope = float(line["Ey"] - line["Sy"]) / float(line["Ex"] - line["Sx"])
    return slope

#find y intercept of line
def find_Y_Intercept(line):
    y_intercept = line["Sy"] - (line["slope"] * line["Sx"])
    return y_intercept
    

with open('parking.json') as data_file:
    data = json.load(data_file)

# Create a black image
#img = np.zeros((512,512,3), np.uint8)
img = cv2.imread('img.jpg')
histogram(img)

verticals = []
horizontals = []
points = {}

for i in range(0,4):
    print(chr(65+i))

    points = {
        "Sx": int(data[chr(65+i)][0]['x']), 
        "Sy": 480 - int(data[chr(65+i)][0]['y']),
        "Ex": int(data[chr(65+i)][1]['x']),
        "Ey": 480 - int(data[chr(65+i)][1]['y'])
    }
    horizontals.append(points)

    cv2.line(img,(points["Sx"],480-points["Sy"]),(points["Ex"],480-points["Ey"]), (255,0,0), 1)
    #Calculate slope for line
    slope = find_Slope(points)

    #add slope and yIntercept
    horizontals[-1]["slope"] = slope
    horizontals[-1]["yInt"] = points["Sy"] - (slope * points["Sx"])
    #print "Hline:", horizontals[-1]["Sx"], horizontals[-1]["Sy"], horizontals[-1]["Ex"], horizontals[-1]["Ey"], horizontals[-1]["slope"], horizontals[-1]["yInt"]


#length of slopes
print "length of hor:", len(horizontals[-1])


verticals.append(
        {
            "Sx": int(data[chr(65+4)][0]['x']),
            "Sy": find_Y_Intersect(horizontals[0], int(data[chr(65+4)][0]['x'])),
            "Ex": int(data[chr(65+4)][1]['x']),
            "Ey": find_Y_Intersect(horizontals[3], int(data[chr(65+4)][1]['x']))
        }
    )

verticals[-1]["slope"] = find_Slope(verticals[-1])
verticals[-1]["yInt"] = find_Y_Intercept(verticals[-1])

points = []
#process vertical lines
for i in range(5,16):
    print "i is", i
    x1 = int(data[chr(65+i)][0]['x'])

    x2 = int(data[chr(65+i)][1]['x'])
    
    #get y intersection value for both x values with 1st and 4th line respectively
    y1 = find_Y_Intersect(horizontals[0], x1)
    y2 = find_Y_Intersect(horizontals[3], x2)
    
    print x1,y1,x2,y2

    #add points to vertical list
    verticals.append(
        {
            "Sx": x1,
            "Sy": y1,
            "Ex": x2,
            "Ey": y2
        }
    )

    #find slope and y intercept for the line
    verticals[-1]["slope"] = find_Slope(verticals[-1])
    verticals[-1]["yInt"] = find_Y_Intercept(verticals[-1])

    print "Vline:",verticals[-1]["Sx"], verticals[-1]["Sy"], verticals[-1]["Ex"], verticals[-1]["Ey"], verticals[-1]["slope"], verticals[-1]["yInt"]
    cv2.line(img, (x1,480-y1), (x2,480-y2), (255,0,0), 1)

    #we need a point object(or array ?) with the top left point and bottom right point
    points = []
    points = [
        {
            'x': verticals[-2]["Sx"],
            'y': verticals[-2]["Sy"]
        }
    ]

    #get intersection of current vertical line and second horizontal line
    intersect_point = lines_intersect(verticals[-1], horizontals[1])
    points.append(
        {
            'x': int(round(intersect_point[0])),
            'y': int(round(intersect_point[1]))
        }
    )

    #print "clipped:", points[0]['x'], points[0]['y'], points[1]['x'], points[1]['y']
    #cut the top parking spot
    cutParkingSpot(img, points, i)

    #print "h2:", horizontals[2]["slope"], horizontals[2]["yInt"]

    #get intersections for previous vertical line with 3rd horizontal, and current vertical with 4th horizontal
    intersect_point = lines_intersect(verticals[-2], horizontals[2])
    intersect_point1 = lines_intersect(verticals[-1], horizontals[3])

    points = [
        {
            'x': int(round(intersect_point[0])),
            'y': int(round(intersect_point[1]))
        },
        {
            'x': int(round(intersect_point1[0])),
            'y': int(round(intersect_point1[1]))
        }
    ]

    #cut parking spot with intersections from above
    print "clipped2:", points[0]['x'], points[0]['y'], points[1]['x'], points[1]['y']
    cutParkingSpot(img, points, i*4)
    print


cv2.imwrite('horz.jpg',img)
#cutParkingSpot(img)

