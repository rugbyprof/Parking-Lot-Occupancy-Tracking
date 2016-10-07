import numpy as np
import cv2
import json

class Point:
        x = 0
        y = 0


class Line:
    startPt = Point()
    endPt = Point()
    slope = 0
    yInt = 0

    def compute_slope(self):
        self.slope = float(self.endPt.y - self.startPt.y) / float(self.endPt.x - self.startPt.x)

    def compute_y_int(self):
        self.yInt = float(self.startPt.y - self.slope*self.startPt.x)
        
    def get_intersect(self, line):
        x = float(self.yInt - line.yInt) / float(line.slope - self.slope)
        y = self.slope*x + self.yInt
        pt = Point(pt, x, y)
        return pt

    def get_y_intersect(self, x):
        y = int(round(self.slope*x + self.yInt))
        return y


        
        

def cutParkingSpot(img, points, idx):
    parkingSpot = img[int(points[0]['y']):int(points[3]['y']), int(points[0]['x']):int(points[3]['x'])]
    new_p_spot = img[int(points[0]['y']):int(points[3]['y']), int(points[0]['x']):int(points[3]['x'])]
    width, height = img.shape[:2]
    print width, height
    res = cv2.resize(parkingSpot, (width/3, height/3), cv2.INTER_LANCZOS4)
    cv2.imshow("spot created", res)
    cv2.imwrite('spot'+str(idx)+'.jpg',res)
    #cv2.imshow("m", img)
    cv2.waitKey(0)
    return

with open('parking.json') as data_file:
    data = json.load(data_file)

# Create a black image
#img = np.zeros((512,512,3), np.uint8)
img = cv2.imread('img.jpg')


lines = []
horizontals = []
points = {}

line = Line()

p = line.get_y_intersect(2)
print p

for i in range(0,4):
    print(chr(65+i))

    points = {
        "Sx": int(data[chr(65+i)][0]['x']), 
        "Sy": int(data[chr(65+i)][0]['y']),
        "Ex": int(data[chr(65+i)][1]['x']),
        "Ey": int(data[chr(65+i)][1]['y'])
    }
    horizontals.append(points)

    cv2.line(img,(points["Sx"],points["Sy"]),(points["Ex"],points["Ey"]), (255,0,0), 1)
    #Calculate slope for line
    slope = float(points["Sy"] - points["Ey"]) / float(points["Ex"] - points["Sx"])

    #append slope and yIntercept
    lines.append(
        {
            "slope": slope,
            "yInt": points["Sy"] - (slope * points["Sx"]) 
        }
    )
    print lines[-1]["slope"]
    print lines[-1]["yInt"]

#length of slopes
print len(lines)

#process vertical lines
for i in range(4,16):
    x1 = int(data[chr(65+i)][0]['x'])
    y1 = int(round(lines[0]["slope"]*x1 + lines[0]["yInt"]))
    y1 = horizontals[0]["Sy"] + (horizontals[0]["Sy"] - y1)

    x2 = int(data[chr(65+i)][1]['x'])
    y2 = int(round(lines[3]["slope"]*x2 + lines[3]["yInt"]))
    print x1,y1,x2,y2

    cv2.line(img, (x1,y1), (x2,y2), (255,0,0), 1)
   # cutParkingSpot(img, data[chr(65+i)], i)


cv2.imwrite('horz.jpg',img)
#cutParkingSpot(img)

